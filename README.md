# Synthetic data Generator


<p>
This project is used to generate Synthetic data for the Database schema (DDL) with the list of all tables provided as input.
</p>

## Input
For example, consider the DDL mentioned in the [schema.sql file](db/schema.sql).

## What does it do?
- When the [main.py](db/main.py) is run it will make sure that it generates synthetic data that adheres to the the **Primary**, **Not Null**, **Unique** and **Referential Integrity** constraints as per the schema definition.
- It generates the necessary DML statements(inserts in this case) and adds all these to `insert.sql` file which gets created inside the **temp** folder of the machine on which it is running. 


## Installation instructions
- Create a Python Virtual Environment.
- Run `pip install -r requirements.txt`.
- Configure the API Keys and Schema definition file values in the .env file.
- Make sure that the DB already exists with the said tables in the schema definition file. The tables are blank and no data is available in it.
- The format of the .env file is as follows:-
  ```
  LLM_MODEL=gpt-4-turbo-2024-04-09
  LLM_MODEL_PROVIDER=openai
  OPENAI_API_KEY=<Your Key>

  # DB Schema Definition
  DB_SCHEMA_FILE=/Users/dhanapathimarepalli/projects/AIGenAI/SyntheticDataGenerator/db/entertainment.sql
  ```
- .env
```
 
#Google
# LLM_MODEL=gemini-2.0-flash-thinking-exp-1219
# LLM_MODEL_PROVIDER=google_genai
# GEMINI_API_KEY =
 
# Langsmith
# LANGSMITH_API_KEY=

# OpenAI
LLM_MODEL=gpt-4-turbo-2024-04-09
LLM_MODEL_PROVIDER=openai
OPENAI_API_KEY=
 
# DB Schema Definition
DB_SCHEMA_FILE=/Users/rushikesh/sarath/SyntheticDataGenerator2/db/schema.sql
DB_SCHEMA_INFO=/Users/rushikesh/sarath/SyntheticDataGit/syntheticdata/dimensions.json

DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=
DB_NAME=synthetic_database
DB_PORT=3306
```
- DB_SCHEMA_FILE : This is the schema file which contains the schemas of all tables.
```sql
CREATE TABLE IF NOT EXISTS Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    PasswordHash VARCHAR(255),
    Phone VARCHAR(15),
    Role ENUM('customer', 'admin') DEFAULT 'customer',
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Categories (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(100),
    Description TEXT
);

CREATE TABLE IF NOT EXISTS Products (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryID INT,
    Name VARCHAR(255),
    Description TEXT,
    Price DECIMAL(10, 2),
    SKU VARCHAR(50) UNIQUE,
    Stock INT,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

CREATE TABLE IF NOT EXISTS Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    TotalAmount DECIMAL(10, 2),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE IF NOT EXISTS OrderItems (
    OrderItemID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    Price DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE IF NOT EXISTS Payments (
    PaymentID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    PaymentDate DATETIME,
    Amount DECIMAL(10, 2),
    Method ENUM('credit_card', 'paypal', 'bank_transfer'),
    Status ENUM('pending', 'completed', 'failed'),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

CREATE TABLE IF NOT EXISTS Shipping (
    ShippingID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    Address VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(100),
    PostalCode VARCHAR(20),
    Country VARCHAR(100),
    ShippedDate DATETIME,
    DeliveryDate DATETIME,
    TrackingNumber VARCHAR(100),
    Carrier VARCHAR(50),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

CREATE TABLE IF NOT EXISTS Reviews (
    ReviewID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    ProductID INT,
    Rating INT CHECK (Rating >= 1 AND Rating <= 5),
    Comment TEXT,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE IF NOT EXISTS Cart (
    CartID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    ProductID INT,
    Quantity INT,
    AddedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
```

- DB_SCHEMA_INFO : This is the json file which contains the contraints for generation of columns for each table.
```json
{
    "Users": {
      "UserID": "Primary key (auto-incremented integer, seq_start)",
      "Name": "Full name of the user max length = 100, NOT UNIQUE",
      "Email": "Unique email address of the user, e.g., user_{seq_start}@gmail.com max length = 100",
      "PasswordHash": "Hashed password for the user max length = 15 NOT UNIQUE",
      "Phone": "Phone number of the user NOT UNIQUE",
      "Role": "User role, either 'customer' or 'admin'",
      "CreatedAt": "Timestamp when the user was created NOT UNIQUE"
    },
    "Categories": {
      "CategoryID": "Primary key (auto-incremented integer, seq_start)",
      "CategoryName": "Name of the category max length = 100 NOT UNIQUE",
      "Description": "Textual description of the category NOT UNIQUE"
    },
    "Products": {
      "ProductID": "Primary key (auto-incremented integer, seq_start)",
      "CategoryID": "Foreign key referencing Categories(CategoryID)",
      "Name": "Product name max length = 255 NOT UNIQUE",
      "Description": "Textual description of the product NOT UNIQUE",
      "Price": "Price of the product DECIMAL(10, 2) NOT UNIQUE",
      "SKU": "Unique Stock Keeping Unit, e.g., sku_{seq_start}@sku.com max length = 50",
      "Stock": "Quantity of the product available in stock NOT UNIQUE",
      "CreatedAt": "Timestamp when the product was added NOT UNIQUE"
    },
    "Orders": {
      "OrderID": "Primary key (auto-incremented integer, seq_start)",
      "UserID": "Foreign key referencing Users(UserID)",
      "OrderDate": "Date and time when the order was placed NOT UNIQUE",
      "Status": "Current status of the order: 'pending', 'processing', 'shipped', 'delivered', or 'cancelled'",
      "TotalAmount": "Total monetary amount of the order DECIMAL(10, 2) NOT UNIQUE"
    },
    "OrderItems": {
      "OrderItemID": "Primary key (auto-incremented integer, seq_start)",
      "OrderID": "Foreign key referencing Orders(OrderID)",
      "ProductID": "Foreign key referencing Products(ProductID) NOT UNIQUE",
      "Quantity": "Number of product units in the order NOT UNIQUE",
      "Price": "Unit price of the product at the time of order DECIMAL(10, 2) NOT UNIQUE"
    },
    "Payments": {
      "PaymentID": "Primary key (auto-incremented integer, seq_start)",
      "OrderID": "Foreign key referencing Orders(OrderID)",
      "PaymentDate": "Date and time when payment was made NOT UNIQUE",
      "Amount": "Amount paid for the order DECIMAL(10, 2) NOT UNIQUE",
      "Method": "Payment method: 'credit_card', 'paypal', or 'bank_transfer'",
      "Status": "Payment status: 'pending', 'completed', or 'failed'"
    },
    "Shipping": {
      "ShippingID": "Primary key (auto-incremented integer, seq_start)",
      "OrderID": "Foreign key referencing Orders(OrderID)",
      "Address": "Street address for delivery max length = 255 NOT UNIQUE",
      "City": "City part of the delivery address max length = 100 NOT UNIQUE",
      "State": "State or province of the delivery address max length = 100 NOT UNIQUE",
      "PostalCode": "Postal or ZIP code of the address NOT UNIQUE",
      "Country": "Country of the delivery address NOT UNIQUE",
      "ShippedDate": "Date the item was shipped NOT UNIQUE",
      "DeliveryDate": "Expected or actual delivery date NOT UNIQUE",
      "TrackingNumber": "Carrier-provided tracking number max length = 100 NOT UNIQUE",
      "Carrier": "Shipping carrier, e.g., FedEx, UPS"
    },
    "Reviews": {
      "ReviewID": "Primary key (auto-incremented integer, seq_start)",
      "UserID": "Foreign key referencing Users(UserID)",
      "ProductID": "Foreign key referencing Products(ProductID)",
      "Rating": "Rating value between 1 and 5",
      "Comment": "Textual feedback or review NOT UNIQUE",
      "CreatedAt": "Timestamp when the review was posted NOT UNIQUE"
    },
    "Cart": {
      "CartID": "Primary key (auto-incremented integer, seq_start)",
      "UserID": "Foreign key referencing Users(UserID)",
      "ProductID": "Foreign key referencing Products(ProductID) NOT UNIQUE",
      "Quantity": "Quantity of the product in the cart NOT UNIQUE",
      "AddedAt": "Timestamp when the item was added to the cart NOT UNIQUE"
    }
  }
  ```