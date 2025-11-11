from app import create_app
from models.database import db

def test_chat_suggestions():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()
    client.post('/login', data={'username':'admin','password':'admin'}, follow_redirects=True)
    rv = client.post('/api/chat', json={'text':'Tôi thích lập trình dữ liệu và AI', 'score':25})
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'suggestions' in data
    assert len(data['suggestions']) > 0
