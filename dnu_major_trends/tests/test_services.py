import json
from app import create_app
from models.database import db

def setup_app():
    app = create_app()
    app.config.update(TESTING=True)
    return app


def test_overview_empty():
    app = setup_app()
    from models.database import MajorData
    with app.app_context():
        db.session.query(MajorData).delete()
        db.session.commit()
    client = app.test_client()
    # login first
    client.post('/login', data={'username':'admin','password':'admin'}, follow_redirects=True)
    rv = client.get('/api/overview', follow_redirects=True)
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['total_students'] == 0

