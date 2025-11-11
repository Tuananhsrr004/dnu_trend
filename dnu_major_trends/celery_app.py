from celery import Celery
from config import DevConfig
from app import create_app
from models.database import db, ForecastCache
from services.analytics import dataframe_from_db
from services.forecasting import forecast_major


def make_celery():
    app = create_app()
    broker_url = DevConfig.__dict__.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    backend_url = DevConfig.__dict__.get('CELERY_RESULT_BACKEND', broker_url)
    celery = Celery(app.import_name, broker=broker_url, backend=backend_url)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery()


@celery.task(name='tasks.update_all_forecasts')
def update_all_forecasts(years: int = 5):
    df = dataframe_from_db()
    majors = sorted(df['major'].dropna().unique().tolist()) if not df.empty else []
    for m in majors:
        payload = forecast_major(m, years)
        # store to cache table
        last = db.session.query(ForecastCache).filter(ForecastCache.major == m).all()
        for row in last:
            db.session.delete(row)
        for item in payload.get('forecast', []):
            db.session.add(ForecastCache(major=m, year=int(item['year']), yhat=float(item['yhat'])))
    db.session.commit()
    return {'majors': majors, 'count': len(majors)}
