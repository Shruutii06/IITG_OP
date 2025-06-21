CREATE DATABASE urban_retail_db;
USE urban_retail_db;
CREATE TABLE Products (
    ProductID VARCHAR(10) PRIMARY KEY,
    Category VARCHAR(50)
);
CREATE TABLE Stores (
    StoreID VARCHAR(10) PRIMARY KEY,
    Region VARCHAR(50)
);
CREATE TABLE InventoryData (
    Date DATE,
    StoreID VARCHAR(10),
    ProductID VARCHAR(10),
    InventoryLevel INT,
    UnitsSold INT,
    UnitsOrdered INT,
    DemandForecast FLOAT,
    Price FLOAT,
    Discount INT,
    HolidayPromotion BOOLEAN,
    WeatherCondition VARCHAR(30),
    CompetitorPricing FLOAT,
    Seasonality VARCHAR(20),
    PRIMARY KEY (Date, StoreID, ProductID),
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
