import pandas as pd

CSV_FILE = "data/clean_brand_dataset.csv"
API_FILE = "data/api_brand_dataset.csv"
OUTPUT_FILE = "data/combined_dataset.csv"

csv_df = pd.read_csv(CSV_FILE)
api_df = pd.read_csv(API_FILE)

print("=" * 60)
print("BRAND VISIBILITY INTELLIGENCE - DATA MERGING")
print("=" * 60)

print("\nCSV dataset:")
print(f"Rows: {len(csv_df)}")
print(f"Columns: {len(csv_df.columns)}")

print("\nAPI dataset:")
print(f"Rows: {len(api_df)}")
print(f"Columns: {len(api_df.columns)}")

csv_df["position"] = pd.NA
csv_df["raw_price"] = pd.NA
csv_df["link"] = pd.NA
csv_df["thumbnail"] = pd.NA

common_columns = [
    "keyword",
    "title",
    "price",
    "raw_price",
    "old_price",
    "extracted_old_price",
    "rating",
    "reviews",
    "platform",
    "position",
    "delivery",
    "link",
    "thumbnail",
    "brand",
    "price_range"
]

for column in common_columns:
    if column not in csv_df.columns:
        csv_df[column] = pd.NA

for column in common_columns:
    if column not in api_df.columns:
        api_df[column] = pd.NA

csv_df = csv_df[common_columns]
api_df = api_df[common_columns]

combined_df = pd.concat(
    [csv_df, api_df],
    ignore_index=True
)

combined_df = combined_df.drop_duplicates().reset_index(drop=True)

combined_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("MERGING COMPLETE")
print("=" * 60)

print(f"\nCombined rows: {len(combined_df)}")
print(f"Combined columns: {len(combined_df.columns)}")

print("\nColumns:")
print(combined_df.columns.tolist())

print("\nRows by data source:")
print(f"Provided CSV: {len(csv_df)}")
print(f"API: {len(api_df)}")

print("\nProducts per keyword:")
print(combined_df["keyword"].value_counts())

print(f"\nSaved to: {OUTPUT_FILE}")