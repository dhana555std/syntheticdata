CREATE TABLE IF NOT EXISTS roles (
    role_id CHAR(36) PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL UNIQUE,
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
);

CREATE TABLE IF NOT EXISTS departments (
    department_id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
);

CREATE TABLE IF NOT EXISTS users (
    user_id CHAR(36) PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    role_id CHAR(36),
    department_id CHAR(36),
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (role_id) REFERENCES roles(role_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
);

CREATE TABLE IF NOT EXISTS vendors (
    vendor_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    contact_email VARCHAR(255),
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
);

CREATE TABLE IF NOT EXISTS products (
    product_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10, 2) NOT NULL,
    vendor_id CHAR(36),
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id CHAR(36) PRIMARY KEY,
    product_id CHAR(36) NOT NULL,
    warehouse_id CHAR(36) NOT NULL,
    quantity INT NOT NULL,
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);

CREATE TABLE IF NOT EXISTS sales_orders (
    order_id CHAR(36) PRIMARY KEY,
    customer_id CHAR(36) NOT NULL,
    order_date TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    status VARCHAR(50) NOT NULL,
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS sales_order_items (
    order_item_id CHAR(36) PRIMARY KEY,
    order_id CHAR(36) NOT NULL,
    product_id CHAR(36) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (order_id) REFERENCES sales_orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS invoices (
    invoice_id CHAR(36) PRIMARY KEY,
    order_id CHAR(36) NOT NULL,
    invoice_date TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    total_amount DECIMAL(12, 2) NOT NULL,
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (order_id) REFERENCES sales_orders(order_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id CHAR(36) PRIMARY KEY,
    invoice_id CHAR(36) NOT NULL,
    payment_date TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    amount_paid DECIMAL(12, 2) NOT NULL,
    payment_method VARCHAR(50),
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    purchase_order_id CHAR(36) PRIMARY KEY,
    supplier_id CHAR(36) NOT NULL,
    order_date TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    status VARCHAR(50),
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE IF NOT EXISTS purchase_order_items (
    po_item_id CHAR(36) PRIMARY KEY,
    purchase_order_id CHAR(36) NOT NULL,
    product_id CHAR(36) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (purchase_order_id) REFERENCES purchase_orders(purchase_order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS accounting_entries (
    entry_id CHAR(36) PRIMARY KEY,
    description TEXT NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    entry_date TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id CHAR(36) PRIMARY KEY,
    customer_id CHAR(36),
    total_amount DECIMAL(12, 2) NOT NULL,
    transaction_date TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS user_preferences (
    preference_id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    preference_key VARCHAR(100) NOT NULL,
    preference_value TEXT,
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS product_tags (
    tag_id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
);

CREATE TABLE IF NOT EXISTS product_tag_mappings (
    mapping_id CHAR(36) PRIMARY KEY,
    product_id CHAR(36) NOT NULL,
    tag_id CHAR(36) NOT NULL,
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (tag_id) REFERENCES product_tags(tag_id)
);

CREATE TABLE IF NOT EXISTS user_sessions (
    session_id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    login_time TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    logout_time TIMESTAMP(3),
    ip_address VARCHAR(45),
    created_by CHAR(36),
    updated_by CHAR(36),
    creation_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_updated_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
