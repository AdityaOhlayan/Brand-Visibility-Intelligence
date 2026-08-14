import pandas as pd

# Load dataset
file_path = "data/brand_dirty_dataset.csv"
df = pd.read_csv(file_path)

print("=" * 60)
print("BRAND VISIBILITY INTELLIGENCE - DATASET INSPECTION")
print("=" * 60)

# 1. Dataset shape
print("\n1. DATASET SHAPE")
print("-" * 40)
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# 2. Column names
print("\n2. COLUMN NAMES")
print("-" * 40)
for column in df.columns:
    print(column)

# 3. Data types
print("\n3. DATA TYPES")
print("-" * 40)
print(df.dtypes)

# 4. Missing values
print("\n4. MISSING VALUES")
print("-" * 40)
missing = df.isnull().sum()
missing_percent = (df.isnull().sum() / len(df)) * 100

missing_report = pd.DataFrame({
    "Missing Count": missing,
    "Missing Percentage": missing_percent.round(2)
})

print(missing_report)

# 5. Unique values
print("\n5. UNIQUE VALUES")
print("-" * 40)

for column in df.columns:
    print(f"\n{column}: {df[column].nunique()} unique values")

# 6. Duplicate rows
print("\n6. DUPLICATE ROWS")
print("-" * 40)
print(f"Duplicate rows: {df.duplicated().sum()}")

# 7. Sample data
print("\n7. FIRST 5 ROWS")
print("-" * 40)
print(df.head().to_string())

# 8. Last 5 rows
print("\n8. LAST 5 ROWS")
print("-" * 40)
print(df.tail().to_string())

# 9. Basic statistics
print("\n9. BASIC STATISTICS")
print("-" * 40)
print(df.describe(include="all").transpose().to_string())

# 10. Object columns and their common values
print("\n10. CATEGORICAL VALUE CHECK")
print("-" * 40)

for column in df.select_dtypes(include="object").columns:
    print(f"\n--- {column} ---")
    print(df[column].value_counts(dropna=False).head(15).to_string())

print("\n" + "=" * 60)
print("INSPECTION COMPLETE")
print("=" * 60)