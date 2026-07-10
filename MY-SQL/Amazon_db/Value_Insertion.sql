INSERT INTO Users (name, email, registered_date, membership) VALUES
('Alice Johnson', 'alice@gmail.com', '2023-01-15', 'Prime'),
('Bob Smith', 'bob@gmail.com', '2023-02-10', 'Basic'),
('Charlie Brown', 'charlie@gmail.com', '2023-03-05', 'Prime'),
('David Lee', 'david@gmail.com', '2023-04-12', 'Basic'),
('Eva Green', 'eva@gmail.com', '2023-05-20', 'Prime');

SELECT * FROM Users;

INSERT INTO Products (product_name, price, category, stock) VALUES
('Echo Dot', 49.99, 'Electronics', 120),
('Kindle Paperwhite', 129.99, 'Books', 50),
('Fire Stick', 39.99, 'Electronics', 80),
('Yoga Mat', 19.99, 'Fitness', 200),
('Wireless Mouse', 24.99, 'Electronics', 150);

INSERT INTO Orders (user_id, order_date, total_amount) VALUES
(1, '2024-05-01', 79.98),
(2, '2024-05-03', 129.99),
(1, '2024-05-04', 49.99),
(3, '2024-05-05', 24.99);

INSERT INTO OrderDetails (order_id, product_id, quantity) VALUES
(1, 1, 2),
(2, 2, 1),
(3, 1, 1),
(4, 5, 1);