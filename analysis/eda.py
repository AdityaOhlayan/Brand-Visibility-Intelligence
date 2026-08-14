import sqlite3
import pandas as pd

DB_FILE = "database/brand_visibility.db"

connection = sqlite3.connect(DB_FILE)

df = pd.read_sql_query(
    "SELECT * FROM products",
    connection
)

connection.close()

print("=" * 70)
print("BRAND VISIBILITY INTELLIGENCE - EDA")
print("=" * 70)

print(f"\nTotal products: {len(df)}")

print("\n" + "=" * 70)
print("GENERAL MARKET ANALYSIS")
print("=" * 70)

print("\n1. Products per keyword")
print(
    df.groupby("keyword")
    .size()
    .sort_values(ascending=False)
)

print("\n2. Overall average price")
print(
    round(df["price"].mean(), 2)
)

print("\n3. Price statistics")
print(
    df["price"].describe()
)

print("\n4. Overall average rating")
print(
    round(df["rating"].mean(), 2)
)

print("\n5. Review statistics")
print(
    df["reviews"].describe()
)

print("\n" + "=" * 70)
print("BRAND ANALYSIS")
print("=" * 70)

print("\n6. Most frequent brands")
print(
    df["brand"]
    .value_counts()
)

print("\n7. Highest average visibility score by brand")
print(
    df.groupby("brand")["visibility_score"]
    .mean()
    .dropna()
    .sort_values(ascending=False)
    .round(2)
)

print("\n8. Average position by brand")
print(
    df.groupby("brand")["position"]
    .mean()
    .dropna()
    .sort_values()
    .round(2)
)

print("\n9. Brands appearing most in top 10")
top_10 = df[df["position"] <= 10]

print(
    top_10["brand"]
    .value_counts()
)

print("\n10. Highest average rating by brand")
print(
    df.groupby("brand")["rating"]
    .mean()
    .dropna()
    .sort_values(ascending=False)
    .round(2)
)

print("\n" + "=" * 70)
print("PRICING ANALYSIS")
print("=" * 70)

print("\n11. Average price by brand")
print(
    df.groupby("brand")["price"]
    .mean()
    .dropna()
    .sort_values(ascending=False)
    .round(2)
)

print("\n12. Products by price range")
print(
    df["price_range"]
    .value_counts()
)

print("\n13. Average position by price range")
print(
    df.groupby("price_range")["position"]
    .mean()
    .dropna()
    .sort_values()
    .round(2)
)

print("\n14. Average price by platform")
print(
    df.groupby("platform")["price"]
    .mean()
    .dropna()
    .sort_values()
    .round(2)
    .head(20)
)

print("\n15. Highest priced product per keyword")

idx = df.groupby("keyword")["price"].idxmax()

print(
    df.loc[
        idx,
        ["keyword", "title", "price"]
    ].sort_values("keyword")
)

print("\n" + "=" * 70)
print("DISCOUNT & OFFER ANALYSIS")
print("=" * 70)

discounted = df[
    df["discount_percentage"] > 0
]

print("\n16. Percentage of products with a non-zero discount")

discount_percentage = (
    len(discounted) / len(df)
) * 100

print(
    f"{discount_percentage:.2f}%"
)

print("\n17. Average position: discounted vs non-discounted")

df["discounted"] = (
    df["discount_percentage"] > 0
)

print(
    df.groupby("discounted")["position"]
    .mean()
    .round(2)
)

print("\n18. Brand with highest average discount")

print(
    df.groupby("brand")["discount_percentage"]
    .mean()
    .dropna()
    .sort_values(ascending=False)
    .round(2)
)

print("\n19. Platform with highest average discount")

print(
    df.groupby("platform")["discount_percentage"]
    .mean()
    .dropna()
    .sort_values(ascending=False)
    .round(2)
    .head(20)
)

print("\n20. Discount vs rating correlation")

print(
    df[
        ["discount_percentage", "rating"]
    ].corr()
)

print("\n" + "=" * 70)
print("PLATFORM ANALYSIS")
print("=" * 70)

print("\n21. Platforms by product count")

print(
    df["platform"]
    .value_counts()
    .head(20)
)

print("\n22. Platform with highest average rating")

print(
    df.groupby("platform")["rating"]
    .mean()
    .dropna()
    .sort_values(ascending=False)
    .round(2)
    .head(20)
)

print("\n23. Platform with lowest average price")

print(
    df.groupby("platform")["price"]
    .mean()
    .dropna()
    .sort_values()
    .round(2)
    .head(20)
)

print("\n24. Average position by platform")

print(
    df.groupby("platform")["position"]
    .mean()
    .dropna()
    .sort_values()
    .round(2)
    .head(20)
)

print("\n25. Most common brands by platform")

platform_brand = (
    df.groupby(
        ["platform", "brand"]
    )
    .size()
    .reset_index(name="count")
    .sort_values(
        ["platform", "count"],
        ascending=[True, False]
    )
)

print(
    platform_brand.head(30)
)

print("\n" + "=" * 70)
print("VISIBILITY & RANKING ANALYSIS")
print("=" * 70)

print("\n26. Ranking distribution")

print(
    df["position"]
    .describe()
)

print("\n27. Highest visibility products")

print(
    df[
        [
            "title",
            "brand",
            "platform",
            "position",
            "visibility_score"
        ]
    ]
    .dropna(subset=["visibility_score"])
    .sort_values(
        "visibility_score",
        ascending=False
    )
    .head(10)
)

print("\n28. Rating vs position correlation")

print(
    df[
        ["rating", "position"]
    ].corr()
)

print("\n29. Reviews vs position correlation")

print(
    df[
        ["reviews", "position"]
    ].corr()
)

print("\n30. Price, rating and reviews correlation with position")

print(
    df[
        [
            "price",
            "rating",
            "reviews",
            "position"
        ]
    ].corr()["position"]
    .sort_values()
)

print("\n" + "=" * 70)
print("EDA COMPLETE")
print("=" * 70)