import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

DB_FILE = "database/brand_visibility.db"

st.set_page_config(
    page_title="Brand Visibility Intelligence",
    page_icon="📊",
    layout="wide"
)


@st.cache_data
def load_data():
    connection = sqlite3.connect(DB_FILE)

    df = pd.read_sql_query(
        "SELECT * FROM products",
        connection
    )

    connection.close()

    return df


df = load_data()

st.title("Brand Visibility Intelligence")
st.caption(
    "Market visibility, pricing, discounts and platform analysis"
)

st.sidebar.header("Filters")

keywords = sorted(
    df["keyword"].dropna().unique()
)

selected_keywords = st.sidebar.multiselect(
    "Keyword",
    keywords,
    default=keywords
)

brands = sorted(
    df["brand"].dropna().unique()
)

selected_brands = st.sidebar.multiselect(
    "Brand",
    brands,
    default=brands
)

platforms = sorted(
    df["platform"].dropna().unique()
)

selected_platforms = st.sidebar.multiselect(
    "Platform",
    platforms,
    default=platforms
)

filtered_df = df[
    df["keyword"].isin(selected_keywords)
    & df["brand"].isin(selected_brands)
    & df["platform"].isin(selected_platforms)
].copy()

st.sidebar.write(
    f"Showing {len(filtered_df):,} products"
)

st.header("Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Products",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "Average Price",
        f"₹{filtered_df['price'].mean():,.0f}"
        if filtered_df["price"].notna().any()
        else "N/A"
    )

with col3:
    st.metric(
        "Average Rating",
        f"{filtered_df['rating'].mean():.2f}"
        if filtered_df["rating"].notna().any()
        else "N/A"
    )

with col4:
    st.metric(
        "Avg Visibility Score",
        f"{filtered_df['visibility_score'].mean():.2f}"
        if filtered_df["visibility_score"].notna().any()
        else "N/A"
    )

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Products by Keyword")

    keyword_counts = (
        filtered_df["keyword"]
        .value_counts()
        .reset_index()
    )

    keyword_counts.columns = [
        "keyword",
        "count"
    ]

    fig = px.bar(
        keyword_counts,
        x="keyword",
        y="count",
        title="Product Distribution by Keyword"
    )

    fig.update_layout(
        xaxis_title="Keyword",
        yaxis_title="Products"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:
    st.subheader("Products by Brand")

    brand_counts = (
        filtered_df["brand"]
        .value_counts()
        .reset_index()
    )

    brand_counts.columns = [
        "brand",
        "count"
    ]

    fig = px.bar(
        brand_counts.head(10),
        x="brand",
        y="count",
        title="Top Brands by Product Count"
    )

    fig.update_layout(
        xaxis_title="Brand",
        yaxis_title="Products"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.subheader("Price Distribution")

price_data = filtered_df.dropna(
    subset=["price"]
)

fig = px.histogram(
    price_data,
    x="price",
    nbins=40,
    title="Product Price Distribution"
)

fig.update_layout(
    xaxis_title="Price",
    yaxis_title="Number of Products"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Platform Distribution")

platform_counts = (
    filtered_df["platform"]
    .value_counts()
    .head(15)
    .reset_index()
)

platform_counts.columns = [
    "platform",
    "count"
]

fig = px.bar(
    platform_counts,
    x="count",
    y="platform",
    orientation="h",
    title="Top Platforms by Product Count"
)

fig.update_layout(
    xaxis_title="Products",
    yaxis_title="Platform"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Top Visible Products")

visible_products = (
    filtered_df[
        filtered_df["visibility_score"].notna()
    ][
        [
            "keyword",
            "title",
            "brand",
            "platform",
            "position",
            "visibility_score",
            "price",
            "rating"
        ]
    ]
    .sort_values(
        "visibility_score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    visible_products,
    use_container_width=True,
    hide_index=True
)