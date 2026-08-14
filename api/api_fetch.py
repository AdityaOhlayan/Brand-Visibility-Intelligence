import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SERPAPI_KEY")

if not api_key:
    raise ValueError("SERPAPI_KEY not found in .env file")

keywords = [
    "microwave oven convection",
    "air fryer India",
    "power bank fast charging",
    "office chair ergonomic",
    "men running shoes"
]

url = "https://serpapi.com/search.json"

all_products = []

for keyword in keywords:

    print(f"\nFetching data for: {keyword}")

    params = {
        "engine": "google_shopping",
        "q": keyword,
        "api_key": api_key,
        "gl": "us",
        "hl": "en"
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    print("HTTP Status:", response.status_code)

    if response.status_code != 200:
        print(f"Request failed for: {keyword}")
        continue

    data = response.json()

    if "error" in data:
        print("SerpAPI Error:", data["error"])
        continue

    products = data.get("shopping_results", [])

    print("Products returned:", len(products))

    for product in products:

        all_products.append({
            "keyword": keyword,
            "title": product.get("title"),
            "price": product.get("extracted_price"),
            "raw_price": product.get("price"),
            "old_price": product.get("old_price"),
            "extracted_old_price": product.get("extracted_old_price"),
            "rating": product.get("rating"),
            "reviews": product.get("reviews"),
            "platform": product.get("source"),
            "position": product.get("position"),
            "delivery": product.get("delivery"),
            "link": product.get("product_link"),
            "thumbnail": product.get("thumbnail")
        })

df = pd.DataFrame(all_products)

output_file = "data/api_brand_dataset.csv"

df.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 60)
print("API EXTRACTION COMPLETE")
print("=" * 60)

print(f"Total API products: {len(df)}")
print(f"Total columns: {len(df.columns)}")

print("\nColumns:")
print(df.columns.tolist())

print("\nProducts per keyword:")
print(df["keyword"].value_counts())

print("\nOld price availability:")
print(df["old_price"].notna().sum())

print("\nExtracted old price availability:")
print(df["extracted_old_price"].notna().sum())

print(f"\nSaved to: {output_file}")