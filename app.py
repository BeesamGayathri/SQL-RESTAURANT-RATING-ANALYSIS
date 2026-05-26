import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Restaurant Consumer Analysis",
    layout="wide"
)

st.title("🍽️ Restaurant Consumer Analysis Dashboard")

# -----------------------------
# LOAD DATASETS
# -----------------------------
consumers = pd.read_csv("datasets/consumers.csv")
restaurants = pd.read_csv("datasets/restaurants.csv")
ratings = pd.read_csv("datasets/ratings.csv")

# -----------------------------
# MERGE DATA
# -----------------------------
df = ratings.merge(
    restaurants,
    on="Restaurant_ID",
    how="left"
)

# -----------------------------
# KPI SECTION
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Restaurants",
    df["Name"].nunique()
)

col2.metric(
    "Average Rating",
    round(df["Overall_Rating"].mean(), 2)
)

col3.metric(
    "Cities",
    df["City"].nunique()
)

# -----------------------------
# TOP RESTAURANTS
# -----------------------------
st.subheader("⭐ Top Rated Restaurants")

top_restaurants = (
    df.groupby("Name")["Overall_Rating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_restaurants,
    x="Name",
    y="Overall_Rating",
    title="Top Rated Restaurants"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# CITY ANALYSIS
# -----------------------------
st.subheader("📍 Ratings by City")

city_rating = (
    df.groupby("City")["Overall_Rating"]
    .mean()
    .reset_index()
)

fig2 = px.pie(
    city_rating,
    names="City",
    values="Overall_Rating",
    title="Average Rating by City"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# RAW DATA
# -----------------------------
st.subheader("📄 Dataset Preview")

st.dataframe(df.head(50))