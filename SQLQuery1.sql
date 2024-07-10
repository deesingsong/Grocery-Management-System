CREATE DATABASE groceries_db

-- Customers table
CREATE TABLE customers (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    email VARCHAR(100) UNIQUE,
    contact_number VARCHAR(20),
	gender VARCHAR(10),
    date_of_birth DATE,
    username VARCHAR(20),
    password VARCHAR(20)
);
ALTER TABLE customers
ADD CONSTRAINT UQ_customers_username UNIQUE (username);

-- Groceries table
CREATE TABLE groceries (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(100) NOT NULL,
    exp_date DATE,
    price DECIMAL(10, 2),
    specification VARCHAR(200)
);

-- Orders table
CREATE TABLE orders (
    id INT PRIMARY KEY IDENTITY(1,1),
    customer_id INT,
    grocery_id INT,
    quantity INT,
    order_date DATE,
    customer_username VARCHAR(20),
    grocery_name VARCHAR(100),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (grocery_id) REFERENCES groceries(id),
    FOREIGN KEY (customer_username) REFERENCES customers(username) ON UPDATE CASCADE
);
UPDATE orders
SET customer_username = customers.username,
    grocery_name = groceries.name
FROM orders
JOIN customers ON orders.customer_id = customers.id
JOIN groceries ON orders.grocery_id = groceries.id;

-- customers info
INSERT INTO customers (name, address, email, contact_number, gender, date_of_birth, username, password)
VALUES
    ('Jonathan', 'Parkhill Residence', 'TP068932@mail.apu.edu.my', '0137668801', 'M', '2002-02-13', 'jonathan', 'jonathan123'),
    ('Adam Farourke', '61, Jalan PJS 9/14', 'adamfarourke@gmail.com', '0196530019', 'M', '2002-09-23', 'adam', 'adam123'),
    ('Ayame Kimura', 'Fortune Park', 'TP063367@mail.apu.edu.my', '0149473819', 'F', '2000-12-25', 'ayame', 'ayame123');

-- groceries info
INSERT INTO groceries (name, exp_date, price, specification)
VALUES
    ('Apples', '2023-07-31', 1.99, 'Fresh and juicy'),
    ('Bananas', '2023-08-15', 0.99, 'Ripe and yellow');

-- orders info
INSERT INTO orders (customer_id, grocery_id, quantity, order_date)
VALUES
    (1, 1, 2, '2023-07-05'),
    (1, 2, 3, '2023-07-06'),
    (2, 2, 1, '2023-07-06');
	
-- test view tables
SELECT * FROM customers
SELECT * FROM groceries
SELECT * FROM orders



-- Backup orders table
CREATE TABLE orders (
    id INT PRIMARY KEY IDENTITY(1,1),
    customer_id INT,
    grocery_id INT,
    quantity INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (grocery_id) REFERENCES groceries(id)
);
ALTER TABLE orders
ADD customer_username VARCHAR(20);
ALTER TABLE orders
ADD CONSTRAINT FK_orders_customers
FOREIGN KEY (customer_username) REFERENCES customers(username);
ALTER TABLE orders
ADD grocery_name VARCHAR(100);
ALTER TABLE orders
DROP CONSTRAINT FK_orders_customers;
ALTER TABLE orders
ADD CONSTRAINT FK_orders_customers
FOREIGN KEY (customer_username) REFERENCES customers(username)
ON UPDATE CASCADE;
UPDATE orders
SET customer_username = customers.username
FROM orders
JOIN customers ON orders.customer_id = customers.id;
UPDATE orders
SET grocery_name = groceries.name
FROM orders
JOIN groceries ON orders.grocery_id = groceries.id;