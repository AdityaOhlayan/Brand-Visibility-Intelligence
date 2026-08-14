import pandas as pd
import re

INPUT_FILE = "data/brand_dirty_dataset.csv"
OUTPUT_FILE = "data/clean_brand_dataset.csv"

print("=" * 60)
print("BRAND VISIBILITY INTELLIGENCE - DATA CLEANING")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)

print(f"\nOriginal rows: {len(df)}")
print(f"Original columns: {len(df.columns)}")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nColumn names standardized.")

text_columns = ["keyword", "title", "platform", "delivery"]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

df["title"] = df["title"].str.replace(
    r"[!]+", "", regex=True
)

df["title"] = df["title"].str.replace(
    r"\s+", " ", regex=True
).str.strip()

df["platform"] = df["platform"].str.lower().str.strip()

platform_mapping = {
    "amazon": "Amazon",
    "flipkart": "Flipkart",
    "croma": "Croma",
    "reliance digital": "Reliance Digital"
}

df["platform"] = df["platform"].replace(platform_mapping)

df["price"] = df["price"].replace(
    ["Not Available", "not available", "N/A", "NA", ""],
    pd.NA
)

df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)

df.loc[df["price"] <= 0, "price"] = pd.NA

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

df.loc[
    (df["rating"] < 0) | (df["rating"] > 5),
    "rating"
] = pd.NA

df["reviews"] = df["reviews"].replace(
    ["many", "Many", "MANY", "N/A", "NA", ""],
    pd.NA
)

df["reviews"] = pd.to_numeric(
    df["reviews"],
    errors="coerce"
)

df.loc[df["reviews"] < 0, "reviews"] = pd.NA

duplicates_before = df.duplicated().sum()

df = df.drop_duplicates().reset_index(drop=True)

print(f"\nDuplicate rows removed: {duplicates_before}")

known_brands = [
    "Apple",
    "Samsung",
    "Dell",
    "HP",
    "Nike",
    "Puma",
    "LG",
    "Philips",
    "Boat"
]

def extract_brand(title):
    if pd.isna(title):
        return "Unknown"

    title = str(title)

    for brand in known_brands:
        if re.search(
            rf"\b{re.escape(brand)}\b",
            title,
            flags=re.IGNORECASE
        ):
            return brand

    return "Unknown"

df["brand"] = df["title"].apply(extract_brand)

def price_category(price):

    if pd.isna(price):
        return "Unknown"

    if price < 1000:
        return "Budget"

    elif price < 5000:
        return "Mid-Range"

    elif price < 20000:
        return "Premium"

    else:
        return "Luxury"

df["price_range"] = df["price"].apply(price_category)

df["price"] = df["price"].astype("float64")
df["rating"] = df["rating"].astype("float64")
df["reviews"] = df["reviews"].astype("Int64")

print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)

print(f"\nFinal rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nData types after cleaning:")
print(df.dtypes)

print("\nPlatforms:")
print(df["platform"].value_counts())

print("\nBrands:")
print(df["brand"].value_counts())

print("\nPrice ranges:")
print(df["price_range"].value_counts())

df.to_csv(OUTPUT_FILE, index=False)

print(f"\nClean dataset saved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 60)
print("CLEANING COMPLETE")
print("=" * 60)