-- =========================================
-- MODULE 10 : SQL ANALYSIS
-- SaaS Churn & Revenue Analytics Platform
-- =========================================

-- Step 1 : Create Database

USE saas_analytics;

-- =========================================
-- Step 3 : Load Data
-- =========================================

-- Import CSV files using MySQL Import Wizard
-- saas_customers.csv
-- saas_subscriptions.csv
-- saas_usage.csv
-- saas_tickets.csv

-- =========================================
-- QUERY 1
-- Total Customers by Industry
-- GROUP BY
-- =========================================

SELECT Industry,
       COUNT(*) AS Total_Customers
FROM clean_customers
GROUP BY Industry
ORDER BY Total_Customers DESC;

-- =========================================
-- QUERY 2
-- Total Revenue by Plan
-- GROUP BY + SUM
-- =========================================

SELECT PlanName,
       ROUND(SUM(MRR),2) AS Total_MRR
FROM clean_subscriptions
GROUP BY PlanName
ORDER BY Total_MRR DESC;

-- =========================================
-- QUERY 3
-- Active Customers with Plan Details
-- INNER JOIN
-- =========================================

SELECT c.CustomerID,
       c.CompanyName,
       s.PlanName,
       s.MRR,
       s.Status
FROM clean_customers c
JOIN clean_subscriptions s
ON c.CustomerID = s.CustomerID
WHERE s.Status = 'Active';

-- =========================================
-- QUERY 4
-- Industries Generating More Than 10000 MRR
-- HAVING
-- =========================================

SELECT c.Industry,
       ROUND(SUM(s.MRR),2) AS Total_MRR
FROM clean_customers c
JOIN clean_subscriptions s
ON c.CustomerID = s.CustomerID
GROUP BY c.Industry
HAVING SUM(s.MRR) > 10000;

-- =========================================
-- QUERY 5
-- Revenue Classification
-- CASE
-- =========================================

SELECT CustomerID,
       PlanName,
       MRR,
       CASE
           WHEN MRR >= 2000 THEN 'High Revenue'
           WHEN MRR >= 500 THEN 'Medium Revenue'
           ELSE 'Low Revenue'
       END AS Revenue_Category
FROM clean_subscriptions;

-- =========================================
-- QUERY 6
-- Average Logins by Customer Status
-- JOIN + AVG
-- =========================================

SELECT s.Status,
       ROUND(AVG(u.Logins),2) AS Avg_Logins
FROM clean_subscriptions s
JOIN clean_usage u
ON s.CustomerID = u.CustomerID
GROUP BY s.Status;

-- =========================================
-- QUERY 7
-- Customers with Highest Ticket Counts
-- GROUP BY
-- =========================================

SELECT CustomerID,
       COUNT(*) AS Total_Tickets
FROM clean_tickets
GROUP BY CustomerID
ORDER BY Total_Tickets DESC;

-- =========================================
-- QUERY 8
-- Customers Having More Tickets Than Average
-- SUBQUERY
-- =========================================

SELECT CustomerID,
       COUNT(*) AS Ticket_Count
FROM clean_tickets
GROUP BY CustomerID
HAVING COUNT(*) >
(
    SELECT AVG(ticket_count)
    FROM
    (
        SELECT COUNT(*) AS ticket_count
        FROM clean_tickets
        GROUP BY CustomerID
    ) t
);

-- =========================================
-- QUERY 9
-- Top Revenue Customers
-- WINDOW FUNCTION
-- =========================================

SELECT CustomerID,
       MRR,
       RANK() OVER(ORDER BY MRR DESC) AS Revenue_Rank
FROM clean_subscriptions;

-- =========================================
-- QUERY 10
-- Running Revenue Total
-- WINDOW FUNCTION
-- =========================================

SELECT CustomerID,
       MRR,
       SUM(MRR) OVER(ORDER BY MRR DESC) AS Running_Total_MRR
FROM clean_subscriptions;

-- =========================================
-- QUERY 11
-- Churned Customers by Industry
-- JOIN + GROUP BY
-- =========================================

SELECT c.Industry,
       COUNT(*) AS Churned_Customers
FROM clean_customers c
JOIN clean_subscriptions s
ON c.CustomerID = s.CustomerID
WHERE s.Status = 'Churned'
GROUP BY c.Industry
ORDER BY Churned_Customers DESC;

-- =========================================
-- QUERY 12
-- Orphan Records
-- Customers present in tickets
-- but missing in subscriptions
-- =========================================

SELECT DISTINCT t.CustomerID
FROM clean_tickets t
LEFT JOIN clean_subscriptions s
ON t.CustomerID = s.CustomerID
WHERE s.CustomerID IS NULL;

-- =========================================
-- QUERY 13
-- CTE Example
-- High Revenue Customers
-- =========================================

WITH HighRevenue AS
(
    SELECT CustomerID,
           SUM(MRR) AS Total_MRR
    FROM clean_subscriptions
    GROUP BY CustomerID
)

SELECT *
FROM HighRevenue
WHERE Total_MRR > 1000;

-- =========================================
-- QUERY 14
-- Monthly Usage Trend
-- =========================================

SELECT Month,
       SUM(Logins) AS Total_Logins
FROM clean_usage
GROUP BY Month
ORDER BY Month;

-- =========================================
-- QUERY 15
-- Top 5 Customers by Login Activity
-- =========================================

SELECT CustomerID,
       SUM(Logins) AS Total_Logins
FROM clean_usage
GROUP BY CustomerID
ORDER BY Total_Logins DESC
LIMIT 5;