import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Restaurant Consumer Analysis",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("🍽️ Restaurant Consumer Analysis")
st.markdown("SQL + Power BI + Streamlit Project")

# -----------------------------------
# LOAD DATA
# -----------------------------------
consumers = pd.read_csv("datasets/consumers.csv")
restaurants = pd.read_csv("datasets/restaurants.csv")
ratings = pd.read_csv("datasets/ratings.csv")

# -----------------------------------
# MERGE TABLES
# -----------------------------------
df = ratings.merge(
    restaurants,
    on="Restaurant_ID",
    how="left"
)

# -----------------------------------
# KPI SECTION
# -----------------------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Restaurants",
    restaurants["Restaurant_ID"].nunique()
)

col2.metric(
    "Average Rating",
    round(ratings["Overall_Rating"].mean(), 2)
)

col3.metric(
    "Total Consumers",
    consumers["Consumer_ID"].nunique()
)

# -----------------------------------
# SQL CONCEPTS SECTION
# -----------------------------------
st.subheader("🧠 SQL Concepts Used")

sql_concepts = [
    "WHERE Clause",
    "GROUP BY",
    "HAVING",
    "JOINS",
    "Subqueries",
    "CTEs",
    "Window Functions",
    "Views",
    "Stored Procedures"
]

st.write(sql_concepts)

# -----------------------------------
# TOP RESTAURANTS
# -----------------------------------
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

# -----------------------------------
# CITY ANALYSIS
# -----------------------------------
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

# -----------------------------------
# CONSUMER ANALYSIS
# -----------------------------------
st.subheader("👥 Consumer Budget Analysis")

budget_count = (
    consumers["Budget"]
    .value_counts()
    .reset_index()
)

budget_count.columns = ["Budget", "Count"]

fig3 = px.bar(
    budget_count,
    x="Budget",
    y="Count",
    title="Consumer Budget Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------
# RAW DATA
# -----------------------------------
st.subheader("📄 Dataset Preview")

st.dataframe(df.head(20))
