"""Check database content"""
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///dnu_trends.sqlite3')
with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) FROM majors_data'))
    count = result.scalar()
    print(f'Total records in database: {count}')
    
    if count > 0:
        result2 = conn.execute(text('SELECT year, major, region, students, male, female FROM majors_data LIMIT 10'))
        print('\nSample data:')
        for row in result2:
            print(f'  {row[0]} - {row[1]} ({row[2]}): {row[3]} students (M:{row[4]}, F:{row[5]})')
    else:
        print('\n⚠️ NO DATA IN DATABASE! Please upload CSV file through the web interface.')
