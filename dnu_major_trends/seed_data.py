import random
from app import create_app
from models.database import db, MajorData

MAJORS = [
    'Công nghệ thông tin',
    'Quản trị kinh doanh',
    'Dược học',
    'Ngôn ngữ Anh',
    'Tài chính - Ngân hàng'
]
REGIONS = ['Bắc', 'Trung', 'Nam']


def run():
    app = create_app()
    with app.app_context():
        # clear existing
        db.session.query(MajorData).delete()
        for year in range(2020, 2025 + 1):
            for major in MAJORS:
                base = random.randint(80, 240)
                for region in REGIONS:
                    # vary by region
                    students = max(10, int(base * random.uniform(0.7, 1.3)))
                    male = int(students * random.uniform(0.4, 0.65))
                    female = students - male
                    avg_score = round(random.uniform(18, 27), 2)
                    db.session.add(MajorData(
                        year=year,
                        major=major,
                        region=region,
                        students=students,
                        male=male,
                        female=female,
                        avg_score=avg_score,
                    ))
        db.session.commit()
        print('Seeded sample data.')


if __name__ == '__main__':
    run()
