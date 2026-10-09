-- ============================================
-- RETAIL SALES ANALYTICS
-- ============================================


-- 1. TOTAL BUSINESS KPIs

SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(net_sales), 2) AS total_revenue,
    ROUND(AVG(net_sales), 2) AS average_order_value,
    SUM(quantity) AS total_units
FROM sales;


-- 2. REVENUE BY COUNTRY

SELECT
    country,
    ROUND(SUM(net_sales), 2) AS revenue
FROM sales
GROUP BY country
ORDER BY revenue DESC;


-- 3. REVENUE BY CATEGORY

SELECT
    category,
    ROUND(SUM(net_sales), 2) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;


-- 4. TOP 10 PRODUCTS

SELECT
    product,
    SUM(quantity) AS units_sold,
    ROUND(SUM(net_sales), 2) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 10;


-- 5. SALES BY CHANNEL

SELECT
    sales_channel,
    COUNT(*) AS orders,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(AVG(net_sales), 2) AS avg_order_value
FROM sales
GROUP BY sales_channel
ORDER BY revenue DESC;


-- 6. MONTHLY SALES

SELECT
    year_month,
    ROUND(SUM(net_sales), 2) AS revenue
FROM sales
GROUP BY year_month
ORDER BY year_month;


-- 7. RETURN RATE

SELECT
    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN returned = 'Yes'
                THEN 1
                ELSE 0
            END
        )
        / COUNT(*),
        2
    ) AS return_rate_percent
FROM sales;


-- 8. AVERAGE CUSTOMER RATING

SELECT
    ROUND(
        AVG(customer_rating),
        2
    ) AS average_rating
FROM sales
WHERE customer_rating IS NOT NULL;


-- 9. TOP CUSTOMERS

SELECT
    customer_id,
    COUNT(*) AS orders,
    ROUND(SUM(net_sales), 2) AS revenue
FROM sales
GROUP BY customer_id
ORDER BY revenue DESC
LIMIT 10;


-- 10. COUNTRY RANKING WITH WINDOW FUNCTION

WITH country_sales AS (
    SELECT
        country,
        SUM(net_sales) AS revenue
    FROM sales
    GROUP BY country
)

SELECT
    country,
    ROUND(revenue, 2) AS revenue,
    RANK() OVER (
        ORDER BY revenue DESC
    ) AS revenue_rank
FROM country_sales;


-- 11. CATEGORY SHARE OF TOTAL REVENUE

WITH category_sales AS (
    SELECT
        category,
        SUM(net_sales) AS revenue
    FROM sales
    GROUP BY category
),

total_sales AS (
    SELECT
        SUM(net_sales) AS total_revenue
    FROM sales
)

SELECT
    category,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        100.0 * revenue / total_revenue,
        2
    ) AS revenue_share_percent
FROM category_sales
CROSS JOIN total_sales
ORDER BY revenue DESC;


-- 12. MONTH-OVER-MONTH GROWTH

WITH monthly_sales AS (
    SELECT
        year_month,
        SUM(net_sales) AS revenue
    FROM sales
    GROUP BY year_month
),

monthly_comparison AS (
    SELECT
        year_month,
        revenue,
        LAG(revenue) OVER (
            ORDER BY year_month
        ) AS previous_month_revenue
    FROM monthly_sales
)

SELECT
    year_month,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        previous_month_revenue,
        2
    ) AS previous_month_revenue,
    ROUND(
        100.0 *
        (
            revenue
            - previous_month_revenue
        )
        / previous_month_revenue,
        2
    ) AS growth_percent
FROM monthly_comparison
ORDER BY year_month;