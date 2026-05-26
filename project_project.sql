CREATE DATABASE IF NOT EXISTS RESTAURANTDB;

USE RESTAURANTDB;

CREATE TABLE IF NOT EXISTS consumers (
    Consumer_ID VARCHAR(10),
    Age INT,
    Occupation VARCHAR(50),
    Budget VARCHAR(20),
    City VARCHAR(50),
    Country VARCHAR(50),
    Marital_Status VARCHAR(30),
    Transportation_Method VARCHAR(50),
    Drink_Level VARCHAR(50),
    Smoker VARCHAR(10)
);
SELECT * FROM consumers;


CREATE TABLE IF NOT EXISTS consumer_preferences (
    Consumer_ID VARCHAR(10),
    Preferred_Cuisine VARCHAR(50)
);

SELECT * FROM consumer_preferences;


CREATE TABLE IF NOT EXISTS ratings (
    Consumer_ID VARCHAR(10),
    Restaurant_ID VARCHAR(10),
    Overall_Rating INT,
    Food_Rating INT,
    Service_Rating INT
);

SELECT * FROM ratings;


CREATE TABLE IF NOT EXISTS restaurant_cuisines (
    Restaurant_ID VARCHAR(10),
    Cuisine VARCHAR(50)
);

SELECT * FROM restaurant_cuisines;

CREATE TABLE restaurants (
    Restaurant_ID VARCHAR(10),
    Name VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50),
    Country VARCHAR(50),
    Zip_Code VARCHAR(20),
    Latitude VARCHAR(30),
    Longitude VARCHAR(30),
    Alcohol_Service VARCHAR(50),
    Smoking_Allowed VARCHAR(30),
    Price VARCHAR(20),
    Franchise VARCHAR(10),
    Area VARCHAR(30),
    Parking VARCHAR(50)
);
DROP TABLE restaurants;


CREATE TABLE restaurants (
    Restaurant_ID VARCHAR(10),
    Name VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50),
    Country VARCHAR(50),
    Zip_Code VARCHAR(20),
    Latitude VARCHAR(30),
    Longitude VARCHAR(30),
    Alcohol_Service VARCHAR(50),
    Smoking_Allowed VARCHAR(30),
    Price VARCHAR(20),
    Franchise VARCHAR(10),
    Area VARCHAR(30),
    Parking VARCHAR(50)
);
SELECT * FROM restaurants;

-- verifying all the tables
SELECT * FROM consumers;
SELECT * FROM consumer_preferences;
SELECT * FROM ratings;
SELECT * FROM restaurant_cuisines;
SELECT * FROM restaurants;

DROP TABLE consumers;

CREATE TABLE consumers (
    Consumer_ID VARCHAR(10),
    City VARCHAR(50),
    State VARCHAR(50),
    Country VARCHAR(50),
    Latitude VARCHAR(30),
    Longitude VARCHAR(30),
    Smoker VARCHAR(10),
    Drink_Level VARCHAR(30),
    Transportation_Method VARCHAR(50),
    Marital_Status VARCHAR(30),
    Children VARCHAR(30),
    Age INT,
    Occupation VARCHAR(50),
    Budget VARCHAR(20)
);

SELECT * FROM consumers;


-- once again verifying the tables in the dataset
-- verifying all the tables
SELECT * FROM consumers;
SELECT * FROM consumer_preferences;
SELECT * FROM ratings;
SELECT * FROM restaurant_cuisines;
SELECT * FROM restaurants;

-- Total Consumers
SELECT COUNT(*) AS Total_Consumers
FROM consumers;

-- Total Restaurants
SELECT COUNT(*) AS Total_Restaurants
FROM restaurants;

-- Consumers from Cuernavaca
SELECT *
FROM consumers
WHERE City = 'Cuernavaca';


-- Restaurants with Medium Price
SELECT Name, City, Price
FROM restaurants
WHERE Price = 'Medium';


-- Restaurants with Overall Rating = 2
SELECT DISTINCT r.Name, r.City
FROM restaurants r
JOIN ratings rt
ON r.Restaurant_ID = rt.Restaurant_ID
WHERE rt.Overall_Rating = 2;

-- RUNNING ADVANCED SQL CONCEPTS
-- -------------------------------------------------- (A)Top 5 Highest Rated Restaurants------------------------------------------------------------------------------------
SELECT r.Name,
       r.City,
       AVG(rt.Overall_Rating) AS Average_Rating
FROM restaurants r
JOIN ratings rt
ON r.Restaurant_ID = rt.Restaurant_ID
GROUP BY r.Restaurant_ID, r.Name, r.City
ORDER BY Average_Rating DESC
LIMIT 5;

-- -----------------------------------------------------------(B) Most Preferred Cuisine -------------------------------------------------
SELECT Preferred_Cuisine,
       COUNT(*) AS Total_Preferences
FROM consumer_preferences
GROUP BY Preferred_Cuisine
ORDER BY Total_Preferences DESC;



-- ------------------------------------------ (C) Average Rating by City ---------------------------------------------------
SELECT r.City,
       AVG(rt.Overall_Rating) AS Avg_Rating
FROM restaurants r
JOIN ratings rt
ON r.Restaurant_ID = rt.Restaurant_ID
GROUP BY r.City
ORDER BY Avg_Rating DESC;

-- -----------------------------------------------(D)Restaurants with Above Average Food Rating-------------------------------------------------
SELECT r.Name,r.City,AVG(rt.Food_Rating) AS Avg_Food_Rating
FROM restaurants r
JOIN ratings rt
ON r.Restaurant_ID = rt.Restaurant_ID
GROUP BY r.Restaurant_ID, r.Name, r.City
HAVING AVG(rt.Food_Rating) >
(
    SELECT AVG(Food_Rating)
    FROM ratings
);

--  -----------------------------------------------(E) Consumers Who Rated More Than 3 Restaurants ---------------------------------------------------------------------------------------------------------
SELECT Consumer_ID,
       COUNT(Restaurant_ID) AS Total_Ratings
FROM ratings
GROUP BY Consumer_ID
HAVING COUNT(Restaurant_ID) > 3;

-- --------------------------------------------------------------(F) Rank Restaurants by Ratings Using Window Function----------------------------------------
SELECT r.Name,r.City,AVG(rt.Overall_Rating) AS Avg_Rating,RANK() OVER (
           ORDER BY AVG(rt.Overall_Rating) DESC
       ) AS Restaurant_Rank
FROM restaurants r
JOIN ratings rt
ON r.Restaurant_ID = rt.Restaurant_ID
GROUP BY r.Restaurant_ID, r.Name, r.City;
-- ----------------------------------------------(G) CTE — Top Rated Restaurants ------------------------------------------------------------------------------------------------
WITH TopRestaurants AS (
    SELECT r.Name,
           r.City,
           AVG(rt.Overall_Rating) AS Avg_Rating
    FROM restaurants r
    JOIN ratings rt
    ON r.Restaurant_ID = rt.Restaurant_ID
    GROUP BY r.Restaurant_ID, r.Name, r.City
)

SELECT * FROM TopRestaurants WHERE Avg_Rating >= 1.5;

-- ----------------------------------------------(H) Create View for Highly Rated Restaurants ---------------------------------------------------------------------------------
CREATE VIEW Highly_Rated_Restaurants AS
SELECT r.Name,
       r.City,
       AVG(rt.Overall_Rating) AS Avg_Rating
FROM restaurants r
JOIN ratings rt
ON r.Restaurant_ID = rt.Restaurant_ID
GROUP BY r.Restaurant_ID, r.Name, r.City
HAVING AVG(rt.Overall_Rating) >= 1.5;

-- ----------------------------------------------(I) Query the View -----------------------------------------------------------------------------------------------------------
SELECT *
FROM Highly_Rated_Restaurants;

-- ----------------------------------------------(J) Stored Procedure Example -------------------------------------------------------------------------------------------------
DELIMITER //

CREATE PROCEDURE GetRestaurantRatings (
    IN min_rating INT
)

BEGIN

SELECT r.Name,
       r.City,
       AVG(rt.Overall_Rating) AS Avg_Rating

FROM restaurants r
JOIN ratings rt
ON r.Restaurant_ID = rt.Restaurant_ID

GROUP BY r.Restaurant_ID, r.Name, r.City

HAVING AVG(rt.Overall_Rating) >= min_rating;

END //

DELIMITER ;


-- ✅ Execute Procedure

CALL GetRestaurantRatings(1);

-- First drop the old view, then recreate it.
DROP VIEW Highly_Rated_Restaurants;

-- Create View Again
CREATE VIEW Highly_Rated_Restaurants AS
SELECT r.Name,
       r.City,
       AVG(rt.Overall_Rating) AS Avg_Rating
FROM restaurants r
JOIN ratings rt
ON r.Restaurant_ID = rt.Restaurant_ID
GROUP BY r.Restaurant_ID, r.Name, r.City
HAVING AVG(rt.Overall_Rating) >= 1.5;


-- DROP AGAIN
DROP VIEW Highly_Rated_Restaurants;

CREATE VIEW Highly_Rated_Restaurants AS
SELECT r.Name,
       r.City,
       AVG(rt.Overall_Rating) AS Avg_Rating
FROM restaurants r
JOIN ratings rt
ON r.Restaurant_ID = rt.Restaurant_ID
GROUP BY r.Restaurant_ID, r.Name, r.City
HAVING AVG(rt.Overall_Rating) >= 1.5;
SELECT *
FROM Highly_Rated_Restaurants;



