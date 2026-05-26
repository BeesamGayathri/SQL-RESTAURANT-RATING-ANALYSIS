import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Restaurant Consumer SQL Analysis",
    page_icon="🍽️",
    layout="wide"
)

# =========================================================
# LOAD DATASETS
# =========================================================
consumers = pd.read_csv("datasets/consumers.csv")
restaurants = pd.read_csv("datasets/restaurants.csv")
ratings = pd.read_csv("datasets/ratings.csv")
cuisines = pd.read_csv("datasets/restaurant_cuisines.csv")
preferences = pd.read_csv("datasets/consumer_preferences.csv")

# =========================================================
# DATA MERGING
# =========================================================
merged_df = ratings.merge(
    restaurants,
    on="Restaurant_ID",
    how="left"
)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("📌 Dashboard Navigation")

section = st.sidebar.radio(
    "Select Section",
    [
        "Project Overview",
        "Restaurant Analysis",
        "Cuisine Analysis",
        "Consumer Analysis",
        "SQL Concepts",
        "Dataset Preview"
    ]
)

# =========================================================
# HEADER IMAGE
# =========================================================
st.image(
    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
    use_container_width=True
)

# =========================================================
# MAIN TITLE
# =========================================================
st.title("🍽️ Restaurant Consumer Analysis")
st.markdown("### Advanced SQL Analytics Dashboard using Streamlit")

st.markdown("---")

# =========================================================
# PROJECT OVERVIEW
# =========================================================
if section == "Project Overview":

    st.image(
        "https://images.unsplash.com/photo-1414235077428-338989a2e8c0",
        use_container_width=True
    )

    st.subheader("📖 Project Overview")

    st.write("""
    This project analyzes restaurant ratings, consumer preferences,
    cuisine trends, and restaurant performance using advanced SQL concepts.

    The analysis focuses on:
    - Consumer behavior analysis
    - Restaurant performance insights
    - Cuisine popularity trends
    - City-wise rating distribution
    - Business insights from relational datasets
    """)

    st.markdown("---")

    st.subheader("📂 Dataset Tables")

    dataset_df = pd.DataFrame({
        "Table Name": [
            "Consumers",
            "Restaurants",
            "Ratings",
            "Restaurant Cuisines",
            "Consumer Preferences"
        ],

        "Description": [
            "Stores demographic and lifestyle information of consumers",
            "Contains restaurant details and services",
            "Stores overall, food, and service ratings",
            "Contains cuisine information for restaurants",
            "Stores preferred cuisines of consumers"
        ]
    })

    st.dataframe(dataset_df, use_container_width=True)

# =========================================================
# RESTAURANT ANALYSIS
# =========================================================
elif section == "Restaurant Analysis":

    st.image(
        "https://images.unsplash.com/photo-1552566626-52f8b828add9",
        use_container_width=True
    )

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
        title="Top 10 Restaurants by Average Rating",
        text_auto=True
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

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

    st.markdown("---")

    st.subheader("💰 Restaurant Pricing Distribution")

    price_dist = (
        restaurants["Price"]
        .value_counts()
        .reset_index()
    )

    price_dist.columns = ["Price", "Count"]

    fig3 = px.bar(
        price_dist,
        x="Price",
        y="Count",
        title="Restaurant Price Categories",
        text_auto=True
    )

    st.plotly_chart(fig3, use_container_width=True)

# =========================================================
# CUISINE ANALYSIS
# =========================================================
elif section == "Cuisine Analysis":

    st.image(
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
        use_container_width=True
    )

    st.subheader("🍜 Most Popular Cuisines")

    cuisine_count = (
        cuisines["Cuisine"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    cuisine_count.columns = ["Cuisine", "Count"]

    fig4 = px.bar(
        cuisine_count,
        x="Cuisine",
        y="Count",
        title="Top 10 Cuisine Types",
        text_auto=True
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    st.subheader("❤️ Consumer Preferred Cuisines")

    pref_count = (
        preferences["Preferred_Cuisine"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    pref_count.columns = ["Preferred Cuisine", "Count"]

    fig5 = px.bar(
        pref_count,
        x="Preferred Cuisine",
        y="Count",
        title="Most Preferred Cuisines by Consumers",
        text_auto=True
    )

    st.plotly_chart(fig5, use_container_width=True)

# =========================================================
# CONSUMER ANALYSIS
# =========================================================
elif section == "Consumer Analysis":

    st.image(
        "https://images.unsplash.com/photo-1529156069898-49953e39b3ac",
        use_container_width=True
    )

    st.subheader("👥 Consumer Budget Distribution")

    budget_count = (
        consumers["Budget"]
        .value_counts()
        .reset_index()
    )

    budget_count.columns = ["Budget", "Count"]

    fig6 = px.bar(
        budget_count,
        x="Budget",
        y="Count",
        title="Consumer Budget Categories",
        text_auto=True
    )

    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("---")

    st.subheader("🚬 Smokers vs Non-Smokers")

    smoker_data = (
        consumers["Smoker"]
        .value_counts()
        .reset_index()
    )

    smoker_data.columns = ["Smoker", "Count"]

    fig7 = px.pie(
        smoker_data,
        names="Smoker",
        values="Count",
        title="Smoking Preference Distribution"
    )

    st.plotly_chart(fig7, use_container_width=True)

    st.markdown("---")

    st.subheader("🚗 Transportation Methods")

    transport_data = (
        consumers["Transportation_Method"]
        .value_counts()
        .reset_index()
    )

    transport_data.columns = ["Transportation", "Count"]

    fig8 = px.bar(
        transport_data,
        x="Transportation",
        y="Count",
        title="Transportation Methods Used by Consumers",
        text_auto=True
    )

    st.plotly_chart(fig8, use_container_width=True)

# =========================================================
# SQL CONCEPTS
# =========================================================
elif section == "SQL Concepts":

    st.subheader("🧠 Advanced SQL Concepts Implemented")

    concepts_df = pd.DataFrame({

        "SQL Concept": [
            "SELECT Statement",
            "WHERE Clause",
            "ORDER BY",
            "GROUP BY",
            "HAVING Clause",
            "Aggregate Functions",
            "INNER JOIN",
            "LEFT JOIN",
            "Subqueries",
            "Nested Queries",
            "Common Table Expressions (CTEs)",
            "Window Functions",
            "RANK() Function",
            "ROW_NUMBER() Function",
            "LEAD() Function",
            "Views",
            "Stored Procedures",
            "Derived Tables",
            "Filtering & Sorting",
            "Business Insight Queries"
        ],

        "Purpose": [
            "Retrieve specific columns from tables",
            "Filter records based on conditions",
            "Sort query results",
            "Group records for analysis",
            "Filter grouped data",
            "Perform calculations like AVG and COUNT",
            "Combine related tables",
            "Retrieve matched and unmatched records",
            "Query inside another query",
            "Perform complex filtering",
            "Improve query readability",
            "Perform analytical calculations",
            "Rank records within partitions",
            "Generate sequential row numbers",
            "Access next row values",
            "Create reusable virtual tables",
            "Automate SQL operations",
            "Create temporary query tables",
            "Improve data exploration",
            "Generate business insights"
        ]
    })

    st.dataframe(concepts_df, use_container_width=True)

    st.markdown("---")

    st.subheader("📌 Sample SQL Queries")

    st.code("""
-- Restaurants with Average Rating Above 1.5

SELECT r.Name,
       AVG(rt.Overall_Rating) AS Avg_Rating
FROM restaurants r
JOIN ratings rt
ON r.Restaurant_ID = rt.Restaurant_ID
GROUP BY r.Name
HAVING AVG(rt.Overall_Rating) > 1.5;
""", language="sql")

    st.code("""
-- Ranking Restaurants Using Window Function

SELECT Restaurant_ID,
       Consumer_ID,
       Overall_Rating,
       RANK() OVER (
           PARTITION BY Restaurant_ID
           ORDER BY Overall_Rating DESC
       ) AS Rating_Rank
FROM ratings;
""", language="sql")

    st.code("""
-- CTE Example

WITH TopRestaurants AS (

    SELECT Restaurant_ID,
           AVG(Overall_Rating) AS Avg_Rating

    FROM ratings
    GROUP BY Restaurant_ID
)

SELECT *
FROM TopRestaurants
WHERE Avg_Rating > 1.5;
""", language="sql")

    st.code("""
-- Stored Procedure Example

CREATE PROCEDURE GetTopRestaurants()

BEGIN

SELECT Name,
       City
FROM restaurants;

END;
""", language="sql")

# =========================================================
# DATASET PREVIEW
# =========================================================
elif section == "Dataset Preview":

    st.subheader("📄 Consumers Dataset")
    st.dataframe(consumers.head(20))

    st.subheader("📄 Restaurants Dataset")
    st.dataframe(restaurants.head(20))

    st.subheader("📄 Ratings Dataset")
    st.dataframe(ratings.head(20))

    st.subheader("📄 Restaurant Cuisines Dataset")
    st.dataframe(cuisines.head(20))

    st.subheader("📄 Consumer Preferences Dataset")
    st.dataframe(preferences.head(20))
