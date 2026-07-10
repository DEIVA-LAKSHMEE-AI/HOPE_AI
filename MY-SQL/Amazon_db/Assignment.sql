#Question 1
SELECT u.user_id,
       u.name,
       u.email,
       o.total_amount
FROM Users u
JOIN Orders o
ON u.user_id = o.user_id
WHERE o.total_amount > 80;

#Question 2
SELECT o.order_id,
       u.name,
       u.email,
       o.order_date,
       o.total_amount
FROM Orders o
JOIN Users u
ON o.user_id = u.user_id;

#Question 3
SELECT category,
       AVG(price) AS average_price
FROM Products
GROUP BY category;

#Question 4
SELECT DISTINCT
    u.user_id,
    u.name,
    u.email
FROM Users u
JOIN Orders o
    ON u.user_id = o.user_id
JOIN OrderDetails od
    ON o.order_id = od.order_id
JOIN Products p
    ON od.product_id = p.product_id
WHERE p.category = 'Electronics';

#Question 5
SELECT
    p.product_id,
    p.product_name,
    SUM(od.quantity) AS total_products_sold,
    SUM(od.quantity * p.price) AS total_revenue
FROM Products p
JOIN OrderDetails od
    ON p.product_id = od.product_id
GROUP BY
    p.product_id,
    p.product_name;
    
#Question 6
UPDATE Products
SET price = price * 1.10
WHERE category = 'Books';

SELECT *
FROM Products
WHERE category = 'Books';

SET SQL_SAFE_UPDATES = 0;

UPDATE Products
SET price = price * 1.10
WHERE category = 'Books';

UPDATE Products
SET price = price * 1.10
WHERE category = 'Books'
AND product_id > 0;

UPDATE Products
SET price = price * 1.10
WHERE category = 'Books'
AND product_id > 0;

SELECT *
FROM Products
WHERE category = 'Books';

#Question 7
SELECT
    u.user_id,
    u.name,
    COUNT(o.order_id) AS total_orders
FROM Users u
LEFT JOIN Orders o
ON u.user_id = o.user_id
GROUP BY u.user_id, u.name;

#question 8
SELECT
    p.category,
    COUNT(p.product_id) AS total_products
FROM Products p
GROUP BY p.category;

#Question 9
SELECT
    p.product_name,
    SUM(od.quantity) AS total_quantity_sold
FROM Products p
JOIN OrderDetails od
ON p.product_id = od.product_id
GROUP BY p.product_name
ORDER BY total_quantity_sold DESC
LIMIT 1;

#Question 10 
SELECT
     p.product_name,
    AVG(o.rating) AS average_rating
FROM Products p
JOIN OrderDetails od
ON p.product_id = od.product_id
JOIN Orders o
ON od.order_id = o.order_id
WHERE p.category = 'Electronics'
GROUP BY p.product_id, p.product_name;

SHOW COLUMNS FROM Orders;
ALTER TABLE Orders
ADD rating DECIMAL(2,1);

UPDATE Orders SET rating = 4.5 WHERE order_id = 1;
UPDATE Orders SET rating = 4.8 WHERE order_id = 2;
UPDATE Orders SET rating = 4.2 WHERE order_id = 3;
UPDATE Orders SET rating = 3.9 WHERE order_id = 4;

SELECT
    p.product_name,
    AVG(o.rating) AS average_rating
FROM Products p
JOIN OrderDetails od
ON p.product_id = od.product_id
JOIN Orders o
ON od.order_id = o.order_id
WHERE p.category = 'Electronics'
GROUP BY p.product_id, p.product_name;

ALTER TABLE Orders
ADD rating DECIMAL(2,1);

UPDATE Orders SET rating = 4.5 WHERE order_id = 1;
UPDATE Orders SET rating = 4.0 WHERE order_id = 2;
UPDATE Orders SET rating = 5.0 WHERE order_id = 3;
UPDATE Orders SET rating = 3.5 WHERE order_id = 4;

SELECT
    p.product_name,
    AVG(o.rating) AS average_rating
FROM Products p
JOIN OrderDetails od
ON p.product_id = od.product_id
JOIN Orders o
ON od.order_id = o.order_id
WHERE p.category = 'Electronics'
GROUP BY p.product_id, p.product_name;

#Question 11
SELECT
    u.name AS Customer_Name,
    p.product_name AS Product_Name,
    SUM(od.quantity) AS Total_Quantity
FROM Users u
JOIN Orders o
ON u.user_id = o.user_id
JOIN OrderDetails od
ON o.order_id = od.order_id
JOIN Products p
ON od.product_id = p.product_id
GROUP BY u.user_id, u.name, p.product_id, p.product_name
HAVING SUM(od.quantity) > 1;

#Question 12

SELECT
    p.category,
    SUM(p.price * od.quantity) AS Total_Revenue
FROM Products p
JOIN OrderDetails od
ON p.product_id = od.product_id
GROUP BY p.category;