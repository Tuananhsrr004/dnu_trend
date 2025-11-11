from app import create_app
from models.database import db, ChatMessage

def test_chat_history_flow():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()
    client.post('/login', data={'username':'admin','password':'admin'}, follow_redirects=True)
    # post a chat
    rv = client.post('/api/chat', json={'text': 'Tôi thích marketing và kinh doanh', 'score': 22})
    assert rv.status_code == 200
    # get history
    rv2 = client.get('/api/chat/history')
    assert rv2.status_code == 200
    data = rv2.get_json()
    assert 'messages' in data and len(data['messages']) >= 1
