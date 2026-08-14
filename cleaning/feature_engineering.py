import pandas as pd
import re

INPUT_FILE = "data/combined_dataset.csv"
OUTPUT_FILE = "data/final_dataset.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("BRAND VISIBILITY INTELLIGENCE - FEATURE ENGINEERING")
print("=" * 60)

print(f"\nInput rows: {len(df)}")
print(f"Input columns: {len(df.columns)}")

df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

df["reviews"] = pd.to_numeric(
    df["reviews"],
    errors="coerce"
)

df["position"] = pd.to_numeric(
    df["position"],
    errors="coerce"
)

df["extracted_old_price"] = pd.to_numeric(
    df["extracted_old_price"],
    errors="coerce"
)

df["old_price"] = df["extracted_old_price"]

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

df["brand"] = df["title"].apply(
    extract_brand
)

def price_category(price):

    if pd.isna(price):
        return "Unknown"

    if price < 1000:
        return "Budget"

    if price < 5000:
        return "Mid-Range"

    if price < 20000:
        return "Premium"

    return "Luxury"

df["price_range"] = df["price"].apply(
    price_category
)

df["visibility_score"] = pd.NA

valid_positions = df["position"].notna()

df.loc[
    valid_positions,
    "visibility_score"
] = (
    (41 - df.loc[valid_positions, "position"])
    / 40
) * 100

df["visibility_score"] = pd.to_numeric(
    df["visibility_score"],
    errors="coerce"
)

df["discount_percentage"] = pd.NA

valid_discount = (
    df["old_price"].notna()
    & df["price"].notna()
    & (df["old_price"] > df["price"])
)

df.loc[
    valid_discount,
    "discount_percentage"
] = (
    (
        df.loc[valid_discount, "old_price"]
        - df.loc[valid_discount, "price"]
    )
    / df.loc[valid_discount, "old_price"]
) * 100

df["discount_percentage"] = pd.to_numeric(
    df["discount_percentage"],
    errors="coerce"
).round(2)

df["price"] = df["price"].astype("float64")
df["raw_price"] = df["raw_price"].astype("string")
df["old_price"] = df["old_price"].astype("float64")
df["extracted_old_price"] = df[
    "extracted_old_price"
].astype("float64")
df["rating"] = df["rating"].astype("float64")
df["reviews"] = df["reviews"].astype("Int64")
df["position"] = df["position"].astype("Int64")
df["visibility_score"] = df[
    "visibility_score"
].astype("float64")
df["discount_percentage"] = df[
    "discount_percentage"
].astype("float64")

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("FEATURE ENGINEERING COMPLETE")
print("=" * 60)

print(f"\nFinal rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")

print("\nColumns:")
print(df.columns.tolist())

print("\nBrand distribution:")
print(df["brand"].value_counts())

print("\nPrice range distribution:")
print(df["price_range"].value_counts())

print("\nVisibility score:")
print(df["visibility_score"].describe())

print("\nDiscount percentage:")
print(df["discount_percentage"].describe())

print("\nProducts with discount:")
print(df["discount_percentage"].notna().sum())

print("\nProducts with ranking:")
print(df["position"].notna().sum())

print(f"\nSaved to: {OUTPUT_FILE}")