-- analysis_queries.sql

-- 1. BASIC QUERY: See all orders
SELECT * FROM orders;

-- 2. FILTERING: Orders from USA customers only
SELECT o.order_id, u.email, u.country, o.amount, o.status
FROM orders o
JOIN users u ON o.user_id = u.user_id
WHERE u.country = 'USA';

-- 3. AGGREGATION: Total sales by country
SELECT 
    u.country,
    COUNT(o.order_id) as total_orders,
    SUM(o.amount) as total_revenue,
    AVG(o.amount) as average_order_value
FROM users u
JOIN orders o ON u.user_id = o.user_id
GROUP BY u.country
ORDER BY total_revenue DESC;

-- 4. CUSTOMER ANALYSIS: Customer lifetime value
SELECT 
    u.user_id,
    u.email,
    u.country,
    COUNT(o.order_id) as order_count,
    SUM(o.amount) as lifetime_value,
    MAX(o.order_date) as last_order_date
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.email, u.country
ORDER BY lifetime_value DESC;

-- 5. PRODUCT PERFORMANCE: Best selling products
SELECT 
    p.product_name,
    p.category,
    COUNT(o.order_id) as times_ordered,
    SUM(o.quantity) as total_quantity,
    SUM(o.amount) as total_revenue
FROM products p
JOIN orders o ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC;