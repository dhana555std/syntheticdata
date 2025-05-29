# Synthetic data Generator


<p>
This project is used to generate Synthetic data for the Database schema (DDL) with the list of all tables provided as input.
</p>

## Input
For example, consider the DDL mentioned in the [schema.sql file](schemas/schema.sql).

## What does it do?
- When the [main.py](db/main.py) is run it will make sure that it generates synthetic data that adheres to the the **Primary**, **Not Null**, **Unique** and **Referential Integrity** constraints as per the schema definition.
- It generates the necessary DML statements(inserts in this case) and adds all these to `insert.sql` file which gets created inside the **temp** folder of the machine on which it is running. 


## Installation instructions
- Create a Python Virtual Environment.
- Run `pip install -r requirements.txt`.
- Configure the API Keys and Schema definition file values in the .env file.
- Make sure that the DB already exists with the said tables in the schema definition file. The tables are blank and no data is available in it.
- The format of the .env file is as follows:-
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

- Work flow : 
  - run `main.py` it will generate the `do` directory which contains the faker files which creates the ouput data.
  - generated data will be stored in `temp/output` dir as json.
  - run `generate_inserts.py` it will generate and insert the data into the db.


---
# Synthetic data Generator

## With AGENT
### CSV synthetic data generation with AGENT 
- required .env 

```
# Gemini
LLM_MODEL=gemini-2.0-flash-thinking-exp-1219
LLM_MODEL_PROVIDER=google_genai
GEMINI_API_KEY =
CSV_DATA_FILE=/Users/rushikesh/sarath/SyntheticDataGit/SyntheticDataCsv/csv_schemas/data.csv
JSON_DATA_FILE=/Users/rushikesh/sarath/SyntheticDataGit/SyntheticDataCsv/json_schemas/nested.json
```

### data.csv : for reference to understamd what kind of data needs to be generated.
```csv
user_id,account_balance,is_active,customer_uuid,signup_date,profile_text,first_name,email_address,personal_website,contact_number,order_status,rating,currency_code,postal_code,country,state,city,notes
123,4567.89,True,550e8400-e29b-41d4-a716-446655440000,2023-04-01 15:30:00,"Loyal customer with frequent purchases","Alice","alice@example.com","https://alice.com","+1-202-555-0123","pending",4,USD,12345,"United States","California","San Francisco","Preferred contact time: mornings"
124,7854.23,False,6a7b8c9d-e0f1-2345-6789-abcdef012345,2022-08-15 11:22:33,"New user exploring features","Bob","bob456@test.org","https://www.bob78.com","+1-303-666-1234","completed",5,EUR,54321,"Canada","Ontario","Toronto","Customer since 2023"
126,1234.56,True,1a2b3c4d-5e6f-7890-1234-567890abcdef,2024-01-20 09:10:11,"Occasional buyer, prefers discounts","Charlie","charlie789@mail.net","https://www.charlie12.com","+1-404-777-5678","shipped",3,GBP,98765,"United Kingdom","England","London","Interested in new features"
129,9876.54,True,fedcba98-7654-3210-fedc-ba9876543210,2023-11-01 20:05:01,"Active community member","Diana","diana123@service.co","https://www.diana34.com","+1-505-888-9012","pending",4,CAD,11223,"Australia","Victoria","Melbourne","Requires email updates"
127,2345.67,False,0a1b2c3d-4e5f-6789-0123-456789abcdef,2022-05-03 07:45:00,"Feedback provider, helps improve services","Eve","eve901@domain.info","https://www.eve56.com","+1-606-999-3456","processing",2,AUD,67890,"Germany","Bavaria","Munich","No specific preferences"
128,8765.43,True,b1c2d3e4-f5a6-7890-1234-567890abcdef,2024-02-29 14:00:00,"Interested in new product releases","Frank","frank234@example.com","https://www.frank89.com","+1-707-111-7890","completed",5,JPY,23456,"Japan","Tokyo","Tokyo","Follow up on recent inquiry"
125,3456.78,False,c2d3e4f5-a6b7-8901-2345-67890abcdef0,2023-07-10 18:15:00,"Long-term subscriber, rarely contacts support","Grace","grace567@test.org","https://www.grace01.com","+1-808-222-2345","shipped",4,USD,78901,"United States","Texas","Austin","VIP customer, provide priority support"
130,6789.01,True,d3e4f5a6-b7c8-9012-3456-7890abcdef01,2022-11-22 03:03:03,"Recently joined, still learning the platform","Henry","henry890@mail.net","https://www.henry23.com","+1-909-333-6789","cancelled",3,EUR,34567,"Canada","Quebec","Montreal","Has expressed interest in premium plan"
131,5432.10,True,e4f5a6b7-c8d9-0123-4567-890abcdef012,2024-03-05 08:00:00,"Loyal customer with frequent purchases","Ivy","ivy012@service.co","https://www.ivy45.com","+1-212-444-0123","pending",5,GBP,89012,"United Kingdom","Scotland","Edinburgh","Preferred contact time: mornings"
133,9012.34,False,f5a6b7c8-d9e0-1234-5678-90abcdef0123,2023-09-19 16:40:00,"New user exploring features","Jack","jack345@domain.info","https://www.jack67.com","+1-313-555-4567","completed",4,CAD,45678,"Australia","Queensland","Brisbane","Customer since 2023"
136,1098.76,True,a6b7c8d9-e0f1-2345-6789-0abcdef01234,2022-07-07 22:00:00,"Occasional buyer, prefers discounts","Karen","karen678@example.com","https://www.karen89.com","+1-414-666-8901","shipped",2,AUD,90123,"Germany","North Rhine-Westphalia","Cologne","Interested in new features"
135,4321.09,False,b7c8d9e0-f1a2-3456-7890-abcdef012345,2024-04-10 13:00:00,"Active community member","Liam","liam901@test.org","https://www.liam01.com","+1-515-777-2345","pending",5,JPY,56789,"Japan","Osaka","Osaka","Requires email updates"
133,7654.32,True,c8d9e0f1-a2b3-4567-8901-234567890abc,2023-02-14 06:30:00,"Feedback provider, helps improve services","Mia","mia123@mail.net","https://www.mia23.com","+1-616-888-6789","processing",3,USD,10112,"United States","New York","New York City","No specific preferences"
132,2109.87,False,d9e0f1a2-b3c4-5678-9012-34567890abcd,2022-10-25 09:45:00,"Interested in new product releases","Noah","noah456@service.co","https://www.noah45.com","+1-717-999-0123","completed",4,EUR,
```
### nested.json : for reference to understamd what kind of data needs to be generated.
```json
{
    "company_details": {
      "company_id": "COMP-XYZ-001",
      "company_name": "Global Tech Innovations Inc.",
      "address": {
        "street": "456 Innovation Drive",
        "suite": "Suite 100",
        "city": "Techville",
        "state_province": "CA",
        "postal_code": "90210",
        "country": "USA",
        "geo_location": {
          "latitude": 34.0522,
          "longitude": -118.2437,
          "timezone": "America/Los_Angeles"
        }
      },
      "contact_info": {
        "main_phone": "+1-555-123-4567",
        "support_email": "support@globaltech.com",
        "departments": {
          "sales": {
            "phone": "+1-555-987-6543",
            "email": "sales@globaltech.com",
            "regional_contacts": [
              {
                "region": "North America",
                "manager": "Alice Smith",
                "email": "alice.s@globaltech.com"
              },
              {
                "region": "Europe",
                "manager": "Bob Johnson",
                "email": "bob.j@globaltech.com"
              }
            ]
          },
          "hr": {
            "phone": "+1-555-222-3333",
            "email": "hr@globaltech.com"
          }
        }
      },
      "products_and_services": [
        {
          "category": "Software",
          "products": [
            {
              "product_id": "SW-APP-001",
              "name": "Cloud Platform Pro",
              "version": "2.1.0",
              "features": [
                {
                  "feature_name": "Data Analytics",
                  "sub_features": [
                    "Real-time Dashboards",
                    "Predictive Modeling"
                  ]
                },
                {
                  "feature_name": "Secure Storage",
                  "encryption_levels": [
                    "AES-256",
                    "RSA-4096"
                  ]
                }
              ],
              "pricing_plans": {
                "basic": {
                  "monthly": 50.00,
                  "annual": 500.00
                },
                "premium": {
                  "monthly": 150.00,
                  "annual": 1500.00
                }
              }
            },
            {
              "product_id": "SW-TOOL-002",
              "name": "DevOps Toolkit",
              "version": "1.5.0"
            }
          ]
        },
        {
          "category": "Hardware",
          "services": [
            {
              "service_id": "HW-CONS-001",
              "name": "Server Installation",
              "service_tiers": ["Standard", "Enterprise"]
            }
          ]
        }
      ],
      "financial_data": {
        "revenue_by_year": {
          "2022": {
            "q1": 10000000,
            "q2": 12000000,
            "q3": 11500000,
            "q4": 13000000
          },
          "2023": {
            "q1": 15000000,
            "q2": 16000000
          }
        },
        "expenses": {
          "operating_costs": {
            "salaries": 5000000,
            "rent": 500000
          },
          "development_costs": 2000000
        }
      },
      "employees": [
        {
          "employee_id": "EMP-001",
          "full_name": "Carol White",
          "position": "CEO",
          "department": "Executive",
          "employment_details": {
            "start_date": "2010-05-01",
            "is_full_time": true,
            "manager": null
          }
        },
        {
          "employee_id": "EMP-002",
          "full_name": "David Green",
          "position": "Lead Developer",
          "department": "Engineering",
          "employment_details": {
            "start_date": "2015-08-15",
            "is_full_time": true,
            "manager": "EMP-001"
          }
        }
      ]
    },
    "system_info": {
      "generated_at": "2023-10-27T10:00:00Z",
      "schema_version": "2.0.0"
    }
  }
```
---

- run `python3 csv_main.py` it will generate `<name of the CSV_DATA_FILE><timestamp>.py` at `./do_csv/` 
  then run this `./do_csv/<name of the CSV_DATA_FILE><timestamp>.py` file to generate the `CSV` data at
  `./generated_csv_data/` as `<name of the CSV_DATA_FILE><timestamp>.csv`

---

## Without AGENT
- This approach does not use the agent, and generated the `CSV` and `JSON` data. 
- Note : Data generated is unique as whole, but can have some repeatations in terms of some field values.

### CSV (same .env content as above)
- run `python3 test_csv.py` file to generate the `CSV` data at
  `./generated_csv_data/` as `<name of the CSV_DATA_FILE><timestamp>.csv`

---


