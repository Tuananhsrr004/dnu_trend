from app import create_app
from models.database import db, User

def test_register_and_login_and_permissions():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    # register new user
    username = 'tester'
    password = 'secret123'
    with app.app_context():
        # ensure clean state if test re-run
        from models.database import User
        u = db.session.query(User).filter_by(username=username).first()
        if u:
            db.session.delete(u)
            db.session.commit()
    rv = client.post('/register', data={'username': username, 'password': password, 'confirm': password}, follow_redirects=True)
    assert rv.status_code == 200

    # should be logged in now, access dashboard OK
    rv2 = client.get('/dashboard')
    assert rv2.status_code == 200

    # non-admin cannot access upload
    rv3 = client.get('/upload')
    assert rv3.status_code == 403

    # admin can access upload
    client.get('/logout')
    client.post('/login', data={'username':'admin','password':'admin'}, follow_redirects=True)
    rv4 = client.get('/upload')
    assert rv4.status_code == 200
