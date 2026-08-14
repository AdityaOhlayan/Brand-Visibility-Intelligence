import sqlite3
import pandas as pd

CSV_FILE = "data/final_dataset.csv"
DB_FILE = "database/brand_visibility.db"

df = pd.read_csv(CSV_FILE)

print("=" * 60)
print("BRAND VISIBILITY INTELLIGENCE - SQL DATABASE")
print("=" * 60)

print(f"\nDataset rows: {len(df)}")
print(f"Dataset columns: {len(df.columns)}")

connection = sqlite3.connect(DB_FILE)

df.to_sql(
    "products",
    connection,
    if_exists="replace",
    index=False
)

print("\nTable created: products")

query = """
SELECT COUNT(*) AS total_products
FROM products
"""

result = pd.read_sql_query(
    query,
    connection
)

print("\nTotal products in database:")
print(result)

query = """
SELECT platform, COUNT(*) AS product_count
FROM products
GROUP BY platform
ORDER BY product_count DESC
"""

result = pd.read_sql_query(
    query,
    connection
)

print("\nProducts by platform:")
print(result)

query = """
SELECT brand, COUNT(*) AS product_count
FROM products
GROUP BY brand
ORDER BY product_count DESC
"""

result = pd.read_sql_query(
    query,
    connection
)

print("\nProducts by brand:")
print(result)

connection.close()

print("\n" + "=" * 60)
print("DATABASE CREATION COMPLETE")
print("=" * 60)

print(f"\nDatabase saved to: {DB_FILE}")