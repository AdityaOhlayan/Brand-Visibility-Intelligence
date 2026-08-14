# Brand Visibility Intelligence

An end-to-end data analytics project that analyzes product visibility, pricing, discounts, ratings, reviews, brands, and e-commerce platforms using a provided dataset and real-time Google Shopping data.

## Overview

Brand Visibility Intelligence combines data from a provided product dataset with product information extracted through the SerpAPI Google Shopping API.

The project follows an ETL and analytics pipeline:

Dirty Dataset + API Data
        ↓
Data Cleaning
        ↓
Data Merging
        ↓
Feature Engineering
        ↓
SQLite Database
        ↓
EDA
        ↓
Streamlit Dashboard

## Features

- Data quality inspection and cleaning
- Missing-value handling
- Duplicate removal
- Invalid price and review handling
- Platform name standardization
- Product brand extraction
- Price-range classification
- Google Shopping API integration using SerpAPI
- Product ranking and visibility score calculation
- Discount percentage calculation
- SQLite database storage
- Exploratory Data Analysis
- Interactive Streamlit dashboard
- Keyword, brand, platform, pricing, and visibility analysis

## Dataset

The project uses five product-search keywords:

- Microwave Oven Convection
- Air Fryer India
- Power Bank Fast Charging
- Office Chair Ergonomic
- Men Running Shoes

The final unified dataset contains:

- 1,434 products
- 17 analytical fields
- 200 products collected through the Google Shopping API

## Technologies Used

- Python
- Pandas
- NumPy
- Requests
- Python-dotenv
- SerpAPI
- SQLite
- SQL
- Streamlit
- Plotly
- Matplotlib
- Seaborn

## Project Structure

```text
Brand-Visibility-Intelligence/
│
├── api/
│   └── api_fetch.py
│
├── analysis/
│   └── eda.py
│
├── cleaning/
│   ├── inspect_data.py
│   ├── clean_data.py
│   ├── merge_data.py
│   └── feature_engineering.py
│
├── dashboard/
│   └── app.py
│
├── database/
│   ├── database.py
│   └── brand_visibility.db
│
├── data/
│   ├── brand_dirty_dataset.csv
│   ├── clean_brand_dataset.csv
│   ├── api_brand_dataset.csv
│   ├── combined_dataset.csv
│   └── final_dataset.csv
│
├── .env
├── .gitignore
└── README.md