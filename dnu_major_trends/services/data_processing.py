import io
from typing import Tuple
import pandas as pd
from werkzeug.datastructures import FileStorage
from sqlalchemy.orm import Session
from models.database import MajorData, db

REQUIRED_COLUMNS = [
    'year', 'major', 'students', 'male', 'female', 'region', 'avg_score'
]


def read_upload(file: FileStorage) -> pd.DataFrame:
    """Read CSV/Excel file from upload to DataFrame with normalized columns."""
    filename = file.filename or ''
    content = file.read()
    buffer = io.BytesIO(content)
    if filename.lower().endswith(('.xlsx', '.xls')):
        df = pd.read_excel(buffer)
    else:
        # default to csv
        df = pd.read_csv(io.BytesIO(content), encoding='utf-8-sig')

    df.columns = [c.strip().lower() for c in df.columns]

    # map Vietnamese-friendly headers if present
    mapping = {
        'năm': 'year',
        'năm tuyển sinh': 'year',
        'ngành': 'major',
        'ngành học': 'major',
        'số lượng sinh viên': 'students',
        'số lượng sinh viên đăng ký': 'students',
        'nam': 'male',
        'nữ': 'female',
        'giới tính': 'gender',
        'khu vực': 'region',
        'điểm chuẩn': 'avg_score',
    }
    for src, dst in mapping.items():
        if src in df.columns and dst not in df.columns:
            df[dst] = df[src]

    # Handle gender column format (if data is split by gender in rows)
    if 'gender' in df.columns and 'male' not in df.columns:
        # Pivot data: convert rows with "Nam"/"Nữ" to separate male/female columns
        df_pivot = df.pivot_table(
            index=['year', 'major', 'region'],
            columns='gender',
            values='students',
            aggfunc='sum',
            fill_value=0
        ).reset_index()
        
        # Rename columns
        df_pivot.columns.name = None
        if 'Nam' in df_pivot.columns:
            df_pivot['male'] = df_pivot['Nam']
        if 'Nữ' in df_pivot.columns:
            df_pivot['female'] = df_pivot['Nữ']
        
        # Calculate total students
        df_pivot['students'] = df_pivot.get('male', 0) + df_pivot.get('female', 0)
        
        df = df_pivot

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            # create missing with sensible defaults
            if col in ('male', 'female'):
                df[col] = 0
            elif col == 'region':
                df[col] = 'Unknown'
            elif col == 'avg_score':
                df[col] = None
            else:
                df[col] = None

    # enforce dtypes
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    df['students'] = pd.to_numeric(df['students'], errors='coerce').fillna(0).astype(int)
    df['male'] = pd.to_numeric(df['male'], errors='coerce').fillna(0).astype(int)
    df['female'] = pd.to_numeric(df['female'], errors='coerce').fillna(0).astype(int)
    df['avg_score'] = pd.to_numeric(df['avg_score'], errors='coerce')
    df['major'] = df['major'].astype(str).str.strip()
    df['region'] = df['region'].astype(str).str.strip()

    # drop rows missing key fields
    df = df.dropna(subset=['year', 'major'])
    return df[REQUIRED_COLUMNS]


def upsert_dataframe(df: pd.DataFrame) -> Tuple[int, int]:
    """Insert or update rows from df into DB. Returns (inserted, updated)."""
    inserted = 0
    updated = 0
    session: Session = db.session

    for _, row in df.iterrows():
        instance = (
            session.query(MajorData)
            .filter_by(year=int(row['year']), major=row['major'], region=row['region'])
            .first()
        )
        if instance:
            # update
            instance.students = int(row['students'])
            instance.male = int(row['male'])
            instance.female = int(row['female'])
            instance.avg_score = float(row['avg_score']) if pd.notna(row['avg_score']) else None
            updated += 1
        else:
            # insert
            instance = MajorData(
                year=int(row['year']),
                major=row['major'],
                students=int(row['students']),
                male=int(row['male']),
                female=int(row['female']),
                region=row['region'],
                avg_score=float(row['avg_score']) if pd.notna(row['avg_score']) else None,
            )
            session.add(instance)
            inserted += 1
    session.commit()
    return inserted, updated
