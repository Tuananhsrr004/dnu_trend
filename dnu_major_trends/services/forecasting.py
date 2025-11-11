from typing import Dict
import warnings
import pandas as pd
from models.database import db, MajorData

# Optional imports with graceful fallback
try:
    from prophet import Prophet  # type: ignore
    HAS_PROPHET = True
except Exception:  # pragma: no cover - environment without prophet
    HAS_PROPHET = False

try:
    from sklearn.linear_model import LinearRegression
    import numpy as np
    HAS_SK = True
except Exception:
    HAS_SK = False

try:
    import statsmodels.api as sm
    HAS_SM = True
except Exception:
    HAS_SM = False


def _history_for_major(major: str) -> pd.DataFrame:
    rows = db.session.query(MajorData).filter(MajorData.major == major).all()
    data = [{'year': r.year, 'students': r.students} for r in rows]
    df = pd.DataFrame(data).sort_values('year')
    return df


def forecast_major(major: str, years_ahead: int = 5) -> Dict:
    df = _history_for_major(major)
    if df.empty or df['year'].nunique() < 2:
        return {'major': major, 'history': [], 'forecast': []}

    if HAS_PROPHET:
        # Prophet expects ds/y with a date-like ds; we'll map year->Jan 1
        p_df = df.rename(columns={'year': 'ds', 'students': 'y'})
        p_df['ds'] = pd.to_datetime(p_df['ds'], format='%Y')
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            model = Prophet()
            model.fit(p_df)
        future = model.make_future_dataframe(periods=years_ahead, freq='Y')
        fc = model.predict(future)
        out = fc[['ds', 'yhat']].copy()
        out['year'] = out['ds'].dt.year
        forecast = out[['year', 'yhat']].to_dict(orient='records')
    elif HAS_SK:
        X = df[['year']].values
        y = df['students'].values
        model = LinearRegression()
        model.fit(X, y)
        last_year = int(df['year'].max())
        future_years = list(range(last_year + 1, last_year + years_ahead + 1))
        preds = model.predict([[y_] for y_ in future_years])
        forecast = [{'year': y_, 'yhat': float(max(0.0, p))} for y_, p in zip(future_years, preds)]
    elif HAS_SM and df.shape[0] >= 3:
        # simple ARIMA(1,1,1) fallback
        series = df.set_index('year')['students']
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            model = sm.tsa.ARIMA(series, order=(1, 1, 1)).fit()
        fc = model.forecast(years_ahead)
        last_year = int(df['year'].max())
        forecast = [
            {'year': last_year + i + 1, 'yhat': float(max(0.0, v))}
            for i, v in enumerate(fc)
        ]
    else:
        # Not enough libs -> naive last value
        last_val = int(df['students'].iloc[-1])
        last_year = int(df['year'].max())
        forecast = [
            {'year': last_year + i + 1, 'yhat': float(last_val)} for i in range(years_ahead)
        ]

    history = df.to_dict(orient='records')
    return {'major': major, 'history': history, 'forecast': forecast}


def top_growth_flags(forecasts: Dict[str, Dict]) -> Dict:
    """Compute percent changes and label growing/shrinking majors."""
    summary = []
    for major, payload in forecasts.items():
        hist = payload.get('history', [])
        fc = payload.get('forecast', [])
        if not hist or not fc:
            continue
        base = hist[-1]['students']
        fut = fc[-1]['yhat']
        pct = (fut - base) / base * 100 if base else 0
        summary.append({'major': major, 'pct_change': pct})
    summary.sort(key=lambda x: x['pct_change'], reverse=True)
    return {
        'top_growing': summary[:5],
        'top_declining': sorted(summary, key=lambda x: x['pct_change'])[:5],
    }
