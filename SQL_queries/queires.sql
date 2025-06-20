-- Query 1
-- Basic Inventory Snapshot
SELECT 
    ProductID, StoreID, Date, InventoryLevel, UnitsSold, UnitsOrdered
FROM InventoryData
ORDER BY Date, StoreID, ProductID;

-- Query 2
-- Inventory Health & Reorder Alerts
-- Static Threshold Check
SELECT 
    ProductID, StoreID, Date, InventoryLevel, DemandForecast,
    CASE 
        WHEN InventoryLevel < DemandForecast * 0.8 THEN 'Below Threshold'
        ELSE 'Safe'
    END AS InventoryStatus
FROM InventoryData
ORDER BY Date;

-- Dynamic Rolling 7-Day Demand Trigger
SELECT
    Date, StoreID, ProductID,
    ROUND(AVG(UnitsSold) OVER (
        PARTITION BY StoreID, ProductID
        ORDER BY Date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 2) AS Avg7DayDemand,
    InventoryLevel,
    CASE
        WHEN InventoryLevel < AVG(UnitsSold) OVER (
            PARTITION BY StoreID, ProductID
            ORDER BY Date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) * 1.5 THEN 'Reorder Now'
        ELSE 'OK'
    END AS Status
FROM InventoryData
ORDER BY Date DESC;

-- Query 3
-- Inventory Turnover
-- Product level
SELECT 
    ProductID,
    ROUND(SUM(UnitsSold) / NULLIF(AVG(InventoryLevel), 0), 2) AS InventoryTurnover
FROM InventoryData
GROUP BY ProductID
ORDER BY InventoryTurnover DESC;

-- Region/Category Level
SELECT
    st.Region, pr.Category,
    ROUND(SUM(id.UnitsSold) * 1.0 / NULLIF(AVG(id.InventoryLevel), 0), 2) AS TurnoverRatio
FROM InventoryData id
JOIN Stores st ON id.StoreID = st.StoreID
JOIN Products pr ON id.ProductID = pr.ProductID
GROUP BY st.Region, pr.Category
ORDER BY TurnoverRatio DESC;

-- Query 4
-- Underperformance & Overstocking
-- Chronic Understocked Products
SELECT
    StoreID, ProductID,
    COUNT(*) AS DaysBelowForecast
FROM InventoryData
WHERE InventoryLevel < DemandForecast
GROUP BY StoreID, ProductID
HAVING COUNT(*) > 7
ORDER BY DaysBelowForecast DESC;

-- Aging inventory alert
WITH HighStock AS (
  SELECT StoreID, ProductID, Date
  FROM InventoryData
  WHERE InventoryLevel > 200
)
SELECT StoreID, ProductID, COUNT(*) AS DaysHighStock
FROM HighStock
GROUP BY StoreID, ProductID
HAVING COUNT(*) > 14
ORDER BY DaysHighStock DESC;

-- Query 5
-- Top & Bottom Performing Products
-- Top 5
SELECT ProductID, SUM(UnitsSold) AS TotalSold
FROM InventoryData
GROUP BY ProductID
ORDER BY TotalSold DESC
LIMIT 5;

-- Bottom 5
SELECT ProductID, SUM(UnitsSold) AS TotalSold
FROM InventoryData
GROUP BY ProductID
ORDER BY TotalSold ASC
LIMIT 5;


-- Query 7
-- external influences
-- weather impact
SELECT WeatherCondition,
    ROUND(AVG(UnitsSold), 2) AS AvgUnitsSold,
    COUNT(*) AS DataPoints
FROM InventoryData
GROUP BY WeatherCondition
ORDER BY AvgUnitsSold DESC;

-- holiday/promotion impact
SELECT HolidayPromotion, AVG(UnitsSold) AS AvgSales
FROM InventoryData
GROUP BY HolidayPromotion;

-- Query 8
-- seasonality and category trends
SELECT Seasonality, pr.Category, id.ProductID, SUM(id.UnitsSold) AS TotalSales
FROM InventoryData id
JOIN Products pr ON id.ProductID = pr.ProductID
GROUP BY Seasonality, pr.Category, id.ProductID
ORDER BY Seasonality, TotalSales DESC;

-- Query 9
-- supply v/s demand gap
SELECT
    ProductID,
    ROUND(AVG(DemandForecast), 2) AS AvgForecast,
    ROUND(AVG(InventoryLevel + UnitsOrdered), 2) AS AvgSupply,
    ROUND(AVG(DemandForecast) - AVG(InventoryLevel + UnitsOrdered), 2) AS AvgSupplyGap
FROM InventoryData
GROUP BY ProductID
ORDER BY AvgSupplyGap DESC;


 


