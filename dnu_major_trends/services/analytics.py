from typing import Dict, List
import pandas as pd
from sqlalchemy.orm import Session
from models.database import MajorData, db


def dataframe_from_db() -> pd.DataFrame:
    session: Session = db.session
    rows = session.query(MajorData).all()
    data = [
        {
            'id': r.id,
            'year': r.year,
            'major': r.major,
            'students': r.students,
            'male': r.male or 0,
            'female': r.female or 0,
            'region': r.region or 'Unknown',
            'avg_score': r.avg_score,
        }
        for r in rows
    ]
    return pd.DataFrame(data)


def overview_stats() -> Dict:
    df = dataframe_from_db()
    if df.empty:
        return {'total_students': 0, 'total_majors': 0, 'years': [], 'top_majors': []}

    total_students = int(df['students'].sum())
    total_majors = df['major'].nunique()
    years = sorted(df['year'].unique().tolist())
    top = (
        df.groupby('major')['students']
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
        .to_dict(orient='records')
    )
    return {
        'total_students': total_students,
        'total_majors': int(total_majors),
        'years': years,
        'top_majors': top,
    }


def trend_by_major(major: str) -> Dict:
    df = dataframe_from_db()
    if df.empty:
        return {'series': []}
    sub = df[df['major'] == major]
    series = (
        sub.groupby('year')['students']
        .sum()
        .sort_index()
        .reset_index()
        .to_dict(orient='records')
    )
    return {'series': series}


def gender_distribution(major: str = None) -> Dict:
    df = dataframe_from_db()
    if df.empty:
        return {'male': 0, 'female': 0}
    if major:
        df = df[df['major'] == major]
    return {
        'male': int(df['male'].sum()),
        'female': int(df['female'].sum()),
    }


def region_distribution(major: str = None) -> Dict:
    df = dataframe_from_db()
    if df.empty:
        return {}
    if major:
        df = df[df['major'] == major]
    series = (
        df.groupby('region')['students']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .to_dict(orient='records')
    )
    return {'series': series}


def heatmap_popularity() -> Dict:
    """Return pivot data: rows=major, cols=year, values=students."""
    df = dataframe_from_db()
    if df.empty:
        return {'majors': [], 'years': [], 'values': []}
    pivot = df.pivot_table(index='major', columns='year', values='students', aggfunc='sum').fillna(0)
    majors = pivot.index.tolist()
    years = pivot.columns.tolist()
    values = pivot.values.tolist()
    return {'majors': majors, 'years': years, 'values': values}


def compare_majors(major_list: List[str] = None) -> Dict:
    """Compare multiple majors over years."""
    df = dataframe_from_db()
    if df.empty:
        return {'series': []}
    
    if major_list:
        df = df[df['major'].isin(major_list)]
    
    result = []
    for major in df['major'].unique():
        major_data = df[df['major'] == major].groupby('year')['students'].sum().reset_index()
        result.append({
            'major': major,
            'data': major_data.to_dict(orient='records')
        })
    
    return {'series': result}


def yearly_summary() -> Dict:
    """Get summary statistics for each year."""
    df = dataframe_from_db()
    if df.empty:
        return {'years': []}
    
    summary = []
    for year in sorted(df['year'].unique()):
        year_data = df[df['year'] == year]
        summary.append({
            'year': int(year),
            'total_students': int(year_data['students'].sum()),
            'total_majors': int(year_data['major'].nunique()),
            'avg_students_per_major': float(year_data.groupby('major')['students'].sum().mean()),
            'top_major': year_data.groupby('major')['students'].sum().idxmax() if not year_data.empty else None
        })
    
    return {'years': summary}
