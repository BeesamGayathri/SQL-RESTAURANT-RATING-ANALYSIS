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
st.markdown("Advanced SQL Project using Streamlit")

# -----------------------------------
# LOAD DATA
# -----------------------------------
consumers = pd.read_csv("datasets/consumers.csv")
restaurants = pd.read_csv("datasets/restaurants.csv")
ratings = pd.read_csv("datasets/ratings.csv")
cuisines = pd.read_csv("datasets/restaurant_cuisines.csv")

# -----------------------------------
# MERGE DATA
# -----------------------------------
df = ratings.merge(
    restaurants,
    on="Restaurant_ID",
    how="left"
)

# -----------------------------------
# KPI SECTION
# -----------------------------------
st.subheader("📊 Project KPIs")

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
# SQL CONCEPTS
# -----------------------------------
st.subheader("🧠 SQL Concepts Used")

sql_concepts = [
    "WHERE Clause",
    "GROUP BY",
    "HAVING",
    "INNER JOIN",
    "Subqueries",
    "CTEs",
    "Window Functions",
    "Views",
    "Stored Procedures"
]

for concept in sql_concepts:
    st.write("✅", concept)

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

fig1 = px.bar(
    top_restaurants,
    x="Name",
    y="Overall_Rating",
    title="Top Rated Restaurants"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------
# CITY ANALYSIS
# -----------------------------------
st.subheader("📍 Average Ratings by City")

city_rating = (
    df.groupby("City")["Overall_Rating"]
    .mean()
    .reset_index()
)

fig2 = px.pie(
    city_rating,
    names="City",
    values="Overall_Rating",
    title="City-wise Ratings"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------
# CUISINE ANALYSIS
# -----------------------------------
st.subheader("🍜 Popular Cuisines")

top_cuisines = (
    cuisines["Cuisine"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_cuisines.columns = ["Cuisine", "Count"]

fig3 = px.bar(
    top_cuisines,
    x="Cuisine",
    y="Count",
    title="Top Cuisine Types"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------
# CONSUMER ANALYSIS
# -----------------------------------
st.subheader("👥 Consumer Budget Distribution")

budget_count = (
    consumers["Budget"]
    .value_counts()
    .reset_index()
)

budget_count.columns = ["Budget", "Count"]

fig4 = px.bar(
    budget_count,
    x="Budget",
    y="Count",
    title="Budget Distribution"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------
# DATA PREVIEW
# -----------------------------------
st.subheader("📄 Dataset Preview")

st.dataframe(df.head(20))
