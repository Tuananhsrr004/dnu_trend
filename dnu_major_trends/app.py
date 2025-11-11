from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from io import BytesIO
import pandas as pd
from functools import wraps

from config import DevConfig
from models.database import init_db, db, User, MajorData, ForecastCache, ChatMessage
from services.data_processing import read_upload, upsert_dataframe
from services.analytics import overview_stats, trend_by_major, gender_distribution, region_distribution, heatmap_popularity, dataframe_from_db, compare_majors, yearly_summary
from services.forecasting import forecast_major, top_growth_flags
from services.chatbot import suggest_majors, llm_proxy_suggestion

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(DevConfig)

    # DB and auth
    init_db(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Ensure admin exists
    with app.app_context():
        if not db.session.query(User).filter_by(username='admin').first():
            admin = User(username='admin', role='admin')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()

    # Pages
    def admin_required(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != 'admin':
                from flask import abort
                abort(403)
            return fn(*args, **kwargs)
        return wrapper

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = (request.form.get('username') or '').strip()
            password = request.form.get('password') or ''
            confirm = request.form.get('confirm') or ''
            if not username or not password:
                flash('Vui lòng nhập đầy đủ thông tin', 'warning')
                return redirect(request.url)
            if password != confirm:
                flash('Mật khẩu xác nhận không khớp', 'danger')
                return redirect(request.url)
            if db.session.query(User).filter_by(username=username).first():
                flash('Tài khoản đã tồn tại', 'danger')
                return redirect(request.url)
            user = User(username=username, role='user')
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Đăng ký thành công!', 'success')
            return redirect(url_for('index'))
        return render_template('register.html')
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = db.session.query(User).filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('index'))
            flash('Sai tài khoản hoặc mật khẩu', 'danger')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/forecast')
    @login_required
    def forecast_page():
        return render_template('forecast.html')

    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def upload():
        # admin only
        if not current_user.is_authenticated or current_user.role != 'admin':
            from flask import abort
            abort(403)
        if request.method == 'POST':
            file = request.files.get('file')
            if not file or file.filename == '':
                flash('Vui lòng chọn file CSV/Excel', 'warning')
                return redirect(request.url)
            ext = file.filename.rsplit('.', 1)[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                flash('Định dạng không hợp lệ', 'danger')
                return redirect(request.url)
            df = read_upload(file)
            inserted, updated = upsert_dataframe(df)
            flash(f'Đã nhập {inserted} mới, cập nhật {updated}', 'success')
            return redirect(url_for('dashboard'))
        return render_template('upload.html')

    @app.route('/reports')
    @login_required
    def reports_page():
        if not current_user.is_authenticated or current_user.role != 'admin':
            from flask import abort
            abort(403)
        return render_template('report.html')

    @app.route('/chat')
    @login_required
    def chat_page():
        return render_template('chat.html')

    @app.route('/debug')
    @login_required
    def debug_page():
        return render_template('debug.html')

    # Test endpoint
    @app.route('/api/test')
    def api_test():
        return jsonify({'status': 'ok', 'message': 'API is working!', 'authenticated': current_user.is_authenticated})

    # APIs
    @app.route('/api/overview')
    @login_required
    def api_overview():
        return jsonify(overview_stats())

    @app.route('/api/majors')
    @login_required
    def api_majors():
        df = dataframe_from_db()
        majors = sorted(df['major'].dropna().unique().tolist()) if not df.empty else []
        return jsonify({'majors': majors})

    @app.route('/api/trend')
    @login_required
    def api_trend():
        major = request.args.get('major')
        return jsonify(trend_by_major(major))

    @app.route('/api/gender')
    @login_required
    def api_gender():
        major = request.args.get('major')
        return jsonify(gender_distribution(major))

    @app.route('/api/region')
    @login_required
    def api_region():
        major = request.args.get('major')
        return jsonify(region_distribution(major))

    @app.route('/api/heatmap')
    @login_required
    def api_heatmap():
        return jsonify(heatmap_popularity())

    @app.route('/api/compare', methods=['POST'])
    @login_required
    def api_compare():
        data = request.get_json(force=True) or {}
        majors = data.get('majors', [])
        return jsonify(compare_majors(majors))

    @app.route('/api/yearly_summary')
    @login_required
    def api_yearly_summary():
        return jsonify(yearly_summary())

    @app.route('/api/forecast')
    @login_required
    def api_forecast():
        major = request.args.get('major')
        years = int(request.args.get('years', 5))
        # try cache first
        cached = (
            db.session.query(ForecastCache)
            .filter(ForecastCache.major == major)
            .order_by(ForecastCache.year)
            .all()
        )
        if cached:
            history = trend_by_major(major)['series']
            payload = {
                'major': major,
                'history': history,
                'forecast': [{'year': c.year, 'yhat': c.yhat} for c in cached]
            }
        else:
            payload = forecast_major(major, years)
        return jsonify(payload)

    @app.route('/api/forecast/summary')
    @login_required
    def api_forecast_summary():
        # generate forecasts for all majors present
        df = dataframe_from_db()
        majors = sorted(df['major'].dropna().unique().tolist()) if not df.empty else []
        all_fc = {m: forecast_major(m, 5) for m in majors}
        summary = top_growth_flags(all_fc)
        return jsonify({'summary': summary, 'majors': majors})

    @app.route('/api/chat', methods=['POST'])
    @login_required
    def api_chat():
        data = request.get_json(force=True) or {}
        prefs = data.get('text', '')
        score = data.get('score')
        top = suggest_majors(prefs, score)
        prompt = llm_proxy_suggestion(prefs)
        # persist message
        import json as _json
        msg = ChatMessage(
            user_id=current_user.id if current_user.is_authenticated else None,
            text=prefs,
            score=float(score) if score not in (None, '') else None,
            suggestions=_json.dumps(top, ensure_ascii=False),
        )
        db.session.add(msg)
        db.session.commit()
        return jsonify({'suggestions': top, 'llm_prompt': prompt, 'message_id': msg.id})

    @app.route('/api/chat/history')
    @login_required
    def api_chat_history():
        # fetch latest 20 messages from current user
        q = db.session.query(ChatMessage)
        if current_user.is_authenticated:
            q = q.filter(ChatMessage.user_id == current_user.id)
        msgs = q.order_by(ChatMessage.created_at.desc()).limit(20).all()
        import json as _json
        out = []
        for m in msgs:
            try:
                sugg = _json.loads(m.suggestions) if m.suggestions else []
            except Exception:
                sugg = []
            out.append({
                'id': m.id,
                'text': m.text,
                'score': m.score,
                'created_at': m.created_at.isoformat(),
                'suggestions': sugg,
            })
        return jsonify({'messages': out})

    # Export endpoints
    @app.route('/export/excel')
    @login_required
    def export_excel():
        if not current_user.is_authenticated or current_user.role != 'admin':
            from flask import abort
            abort(403)
        df = dataframe_from_db()
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='MajorsData')
        output.seek(0)
        return send_file(output, download_name='majors_data.xlsx', as_attachment=True)

    @app.route('/export/pdf')
    @login_required
    def export_pdf():
        if not current_user.is_authenticated or current_user.role != 'admin':
            from flask import abort
            abort(403)
        # lightweight PDF summary
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        stats = overview_stats()
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, "DNU Major Trends - Tổng quan")
        c.setFont("Helvetica", 12)
        c.drawString(50, 770, f"Tổng số SV: {stats['total_students']}")
        c.drawString(50, 750, f"Số ngành: {stats['total_majors']}")
        c.drawString(50, 730, f"Năm: {', '.join(map(str, stats['years']))}")
        c.drawString(50, 710, "Top ngành:")
        y = 690
        for item in stats['top_majors']:
            c.drawString(70, y, f"{item['major']}: {item['students']}")
            y -= 20
        c.showPage()
        c.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='overview.pdf')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
