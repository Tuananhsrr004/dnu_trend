"""Initialize database tables"""
from app import create_app
from models.database import db

app = create_app()
with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("✅ Database tables created successfully!")
    
    # List all tables
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"\nTables in database: {tables}")
