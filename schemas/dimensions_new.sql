
CREATE TABLE DimDate (
    DateKey INT PRIMARY KEY,
    Date DATE,
    Day INT,
    Month INT,
    Year INT,
    Quarter INT,
    Week INT,
    DayOfWeek INT
);

CREATE TABLE DimUser (
    UserKey INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Role VARCHAR(50)
);

CREATE TABLE DimProduct (
    ProductKey INT PRIMARY KEY AUTO_INCREMENT,
    ProductID INT,
    Name VARCHAR(255),
    CategoryName VARCHAR(100),
    SKU VARCHAR(50)
);

CREATE TABLE DimCategory (
    CategoryKey INT PRIMARY KEY AUTO_INCREMENT,
    CategoryID INT,
    CategoryName VARCHAR(100),
    Description TEXT
);

CREATE TABLE DimShipping (
    ShippingKey INT PRIMARY KEY AUTO_INCREMENT,
    Carrier VARCHAR(50),
    Country VARCHAR(100),
    City VARCHAR(100),
    State VARCHAR(100),
    PostalCode VARCHAR(20)
);

CREATE TABLE DimPaymentMethod (
    PaymentMethodKey INT PRIMARY KEY AUTO_INCREMENT,
    Method VARCHAR(50)
);

CREATE TABLE FactOrders (
    OrderKey INT PRIMARY KEY AUTO_INCREMENT,
    UserKey INT,
    ProductKey INT,
    DateKey INT,
    Quantity INT,
    Price DECIMAL(10, 2),
    TotalAmount DECIMAL(10, 2),
    FOREIGN KEY (UserKey) REFERENCES DimUser(UserKey),
    FOREIGN KEY (ProductKey) REFERENCES DimProduct(ProductKey),
    FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey)
);

CREATE TABLE FactPayments (
    PaymentKey INT PRIMARY KEY AUTO_INCREMENT,
    OrderKey INT,
    PaymentMethodKey INT,
    DateKey INT,
    Amount DECIMAL(10, 2),
    FOREIGN KEY (OrderKey) REFERENCES FactOrders(OrderKey),
    FOREIGN KEY (PaymentMethodKey) REFERENCES DimPaymentMethod(PaymentMethodKey),
    FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey)
);

CREATE TABLE FactShipping (
    ShippingKey INT PRIMARY KEY AUTO_INCREMENT,
    OrderKey INT,
    ShippingDateKey INT,
    DeliveryDateKey INT,
    ShippingCost DECIMAL(10, 2),
    ShippingMethod VARCHAR(100),
    FOREIGN KEY (OrderKey) REFERENCES FactOrders(OrderKey),
    FOREIGN KEY (ShippingDateKey) REFERENCES DimDate(DateKey),
    FOREIGN KEY (DeliveryDateKey) REFERENCES DimDate(DateKey)
);