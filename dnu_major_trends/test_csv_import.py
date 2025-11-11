"""Test script to verify CSV import logic"""
import pandas as pd
from io import BytesIO

# Simulate file reading
with open('sample_data/du_lieu_chon_nganh_2020_2024.csv', 'rb') as f:
    content = f.read()

buffer = BytesIO(content)
df = pd.read_csv(buffer, encoding='utf-8-sig')

print("=" * 60)
print("ORIGINAL CSV DATA")
print("=" * 60)
print(f"Shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst 10 rows:")
print(df.head(10))
print(f"\nData types:")
print(df.dtypes)
print(f"\nUnique values in 'Giới tính': {df['Giới tính'].unique()}")

# Test the transformation
df.columns = [c.strip().lower() for c in df.columns]
print("\n" + "=" * 60)
print("AFTER COLUMN NORMALIZATION")
print("=" * 60)
print(f"Columns: {df.columns.tolist()}")

# Apply mapping
mapping = {
    'năm': 'year',
    'ngành': 'major',
    'số lượng sinh viên': 'students',
    'giới tính': 'gender',
    'khu vực': 'region',
}
for src, dst in mapping.items():
    if src in df.columns and dst not in df.columns:
        df[dst] = df[src]

print(f"\nAfter mapping:")
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst 5 rows:")
print(df[['year', 'major', 'students', 'gender', 'region']].head())

# Test pivot
print("\n" + "=" * 60)
print("PIVOT TRANSFORMATION (Gender to Male/Female columns)")
print("=" * 60)

df_pivot = df.pivot_table(
    index=['year', 'major', 'region'],
    columns='gender',
    values='students',
    aggfunc='sum',
    fill_value=0
).reset_index()

df_pivot.columns.name = None
print(f"Pivot shape: {df_pivot.shape}")
print(f"Pivot columns: {df_pivot.columns.tolist()}")
print(f"\nFirst 10 rows of pivot:")
print(df_pivot.head(10))

# Add male/female columns
if 'Nam' in df_pivot.columns:
    df_pivot['male'] = df_pivot['Nam']
if 'Nữ' in df_pivot.columns:
    df_pivot['female'] = df_pivot['Nữ']

df_pivot['students'] = df_pivot.get('male', 0) + df_pivot.get('female', 0)

print("\n" + "=" * 60)
print("FINAL RESULT")
print("=" * 60)
print(f"Final shape: {df_pivot.shape}")
print(f"Final columns: {df_pivot.columns.tolist()}")
print(f"\nFinal data (showing year, major, region, male, female, students):")
result = df_pivot[['year', 'major', 'region', 'male', 'female', 'students']]
print(result.head(15))

print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)
print(f"Total unique majors: {result['major'].nunique()}")
print(f"Majors: {sorted(result['major'].unique())}")
print(f"Years: {sorted(result['year'].unique())}")
print(f"Regions: {sorted(result['region'].unique())}")
print(f"Total students: {result['students'].sum():,}")
print(f"Total male: {result['male'].sum():,}")
print(f"Total female: {result['female'].sum():,}")
