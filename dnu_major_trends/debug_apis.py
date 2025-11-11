"""
Debug script - Test if APIs work
"""
from app import create_app
from models.database import db, MajorData

app = create_app()

with app.app_context():
    # Check database
    count = db.session.query(MajorData).count()
    print(f"📊 Total records in database: {count}")
    
    if count == 0:
        print("⚠️ NO DATA! Running seed_data.py...")
        import seed_data
        seed_data.main()
        count = db.session.query(MajorData).count()
        print(f"✅ After seeding: {count} records")
    
    # Test overview API
    from services.analytics import overview_stats
    result = overview_stats()
    print(f"\n📈 Overview API Result:")
    print(f"  - Total students: {result.get('total_students')}")
    print(f"  - Total majors: {result.get('total_majors')}")
    print(f"  - Top majors: {result.get('top_majors')}")
    
    # Test heatmap API
    from services.analytics import heatmap_popularity
    hm = heatmap_popularity()
    print(f"\n🗺️ Heatmap API Result:")
    print(f"  - Years: {hm.get('years')}")
    print(f"  - Majors count: {len(hm.get('majors', []))}")
    print(f"  - Values shape: {len(hm.get('values', []))} x {len(hm.get('values', [[]])[0]) if hm.get('values') else 0}")
    
    # Test majors API
    from services.analytics import dataframe_from_db
    df = dataframe_from_db()
    majors = sorted(df['major'].dropna().unique().tolist()) if not df.empty else []
    print(f"\n🎓 Majors List ({len(majors)}):")
    for m in majors[:5]:
        print(f"  - {m}")
    
    print("\n✅ All APIs working correctly!")
