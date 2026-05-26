import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Restaurant Consumer SQL Analysis",
    page_icon="🍽️",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
consumers = pd.read_csv("datasets/consumers.csv")
restaurants = pd.read_csv("datasets/restaurants.csv")
ratings = pd.read_csv("datasets/ratings.csv")
cuisines = pd.read_csv("datasets/restaurant_cuisines.csv")

# ---------------------------------------------------
# DATA MERGING
# ---------------------------------------------------
merged_df = ratings.merge(
    restaurants,
    on="Restaurant_ID",
    how="left"
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("📌 Navigation")

section = st.sidebar.radio(
    "Go To",
    [
        "Project Overview",
        "Restaurant Analysis",
        "Cuisine Analysis",
        "Consumer Analysis",
        "SQL Concepts",
        "Dataset Preview"
    ]
)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("🍽️ Restaurant Consumer Analysis")
st.markdown("### Advanced SQL Analytics Dashboard")

st.markdown("---")

# ---------------------------------------------------
# PROJECT OVERVIEW
# ---------------------------------------------------
if section == "Project Overview":

    st.subheader("📖 Project Overview")

    st.write("""
    This project analyzes restaurant ratings, consumer preferences,
    cuisines, and restaurant performance using advanced SQL concepts.

    The analysis focuses on:
    - Consumer behavior
    - Restaurant ratings
    - Cuisine popularity
    - City-wise restaurant performance
    - Business insights from relational datasets
    """)

    st.subheader("🧠 SQL Concepts Used")

    concepts = pd.DataFrame({
        "SQL Concepts": [
            "WHERE Clause",
            "GROUP BY",
            "HAVING",
            "INNER JOIN",
            "Subqueries",
            "Common Table Expressions (CTEs)",
            "Window Functions",
            "Views",
            "Stored Procedures"
        ]
    })

    st.table(concepts)

# ---------------------------------------------------
# RESTAURANT ANALYSIS
# ---------------------------------------------------
elif section == "Restaurant Analysis":

    st.subheader("⭐ Top Rated Restaurants")

    top_restaurants = (
        merged_df.groupby("Name")["Overall_Rating"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig1 = px.bar(
        top_restaurants,
        x="Name",
        y="Overall_Rating",
        title="Top 10 Restaurants by Average Rating"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📍 City-wise Restaurant Ratings")

    city_rating = (
        merged_df.groupby("City")["Overall_Rating"]
        .mean()
        .reset_index()
    )

    fig2 = px.pie(
        city_rating,
        names="City",
        values="Overall_Rating",
        title="Average Ratings by City"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# CUISINE ANALYSIS
# ---------------------------------------------------
elif section == "Cuisine Analysis":

    st.subheader("🍜 Most Popular Cuisines")

    cuisine_count = (
        cuisines["Cuisine"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    cuisine_count.columns = ["Cuisine", "Count"]

    fig3 = px.bar(
        cuisine_count,
        x="Cuisine",
        y="Count",
        title="Top 10 Cuisine Types"
    )

    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# CONSUMER ANALYSIS
# ---------------------------------------------------
elif section == "Consumer Analysis":

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
        title="Consumer Budget Categories"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("🚬 Smokers vs Non-Smokers")

    smoker_data = (
        consumers["Smoker"]
        .value_counts()
        .reset_index()
    )

    smoker_data.columns = ["Smoker", "Count"]

    fig5 = px.pie(
        smoker_data,
        names="Smoker",
        values="Count",
        title="Smoking Preference Distribution"
    )

    st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------
# SQL CONCEPTS
# ---------------------------------------------------
elif section == "SQL Concepts":

    st.subheader("🧠 Advanced SQL Queries Used")

    st.code("""
-- Restaurants with Average Rating > 1.5

SELECT r.Name,
       AVG(rt.Overall_Rating) AS Avg_Rating
FROM restaurants r
JOIN ratings rt
ON r.Restaurant_ID = rt.Restaurant_ID
GROUP BY r.Name
HAVING AVG(rt.Overall_Rating) > 1.5;
""", language="sql")

    st.code("""
-- Window Function Example

SELECT Consumer_ID,
       Restaurant_ID,
       Overall_Rating,
       RANK() OVER (
           PARTITION BY Consumer_ID
           ORDER BY Overall_Rating DESC
       ) AS Rating_Rank
FROM ratings;
""", language="sql")

# ---------------------------------------------------
# DATASET PREVIEW
# ---------------------------------------------------
elif section == "Dataset Preview":

    st.subheader("📄 Restaurants Dataset")
    st.dataframe(restaurants.head(20))

    st.subheader("📄 Consumers Dataset")
    st.dataframe(consumers.head(20))

    st.subheader("📄 Ratings Dataset")
    st.dataframe(ratings.head(20))
