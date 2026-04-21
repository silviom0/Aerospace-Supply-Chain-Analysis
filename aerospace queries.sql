-- =============================================================
-- aerospace_queries.sql
-- Schema + analytical queries for the aerospace supply chain DB
-- Compatible with PostgreSQL (and SQLite with minor tweaks)
-- =============================================================

-- ─── CREATE TABLE ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS aerospace_supply_chain (
    Order_ID                VARCHAR(12)    PRIMARY KEY,
    Part_Name               VARCHAR(60)    NOT NULL,
    Supplier_Location       VARCHAR(40)    NOT NULL,
    Expected_Delivery_Days  INT            NOT NULL,
    Actual_Delivery_Days    INT            NOT NULL,
    Shipping_Cost           NUMERIC(12, 2),
    Defect_Rate             NUMERIC(6, 4)
);

-- ─── LOAD DATA (PostgreSQL COPY command) ─────────────────────
-- COPY aerospace_supply_chain
-- FROM '/path/to/aerospace_supply_chain_clean.csv'
-- DELIMITER ',' CSV HEADER;


-- ─── QUERY 1: Top 5 Most Expensive Delayed Parts ─────────────
-- Finds parts where actual delivery exceeded expected,
-- ranked by average shipping cost of the delayed orders.
SELECT
    Part_Name,
    COUNT(*)                                AS Delayed_Orders,
    ROUND(AVG(Shipping_Cost), 2)            AS Avg_Shipping_Cost,
    ROUND(AVG(Actual_Delivery_Days
              - Expected_Delivery_Days), 1) AS Avg_Delay_Days,
    ROUND(SUM(Shipping_Cost), 2)            AS Total_Spend
FROM aerospace_supply_chain
WHERE Actual_Delivery_Days > Expected_Delivery_Days
GROUP BY Part_Name
ORDER BY Avg_Shipping_Cost DESC
LIMIT 5;


-- ─── QUERY 2: Worst Defect Rate by Supplier Region ───────────
SELECT
    Supplier_Location,
    COUNT(*)                        AS Total_Orders,
    ROUND(AVG(Defect_Rate) * 100, 3) AS Avg_Defect_Pct,
    ROUND(AVG(Shipping_Cost), 2)    AS Avg_Cost,
    ROUND(AVG(Actual_Delivery_Days
              - Expected_Delivery_Days), 2) AS Avg_Delay_Days
FROM aerospace_supply_chain
GROUP BY Supplier_Location
ORDER BY Avg_Defect_Pct DESC;


-- ─── QUERY 3: On-Time Delivery Rate per Region ───────────────
SELECT
    Supplier_Location,
    COUNT(*)                                           AS Total_Orders,
    SUM(CASE WHEN Actual_Delivery_Days
                   <= Expected_Delivery_Days THEN 1
             ELSE 0 END)                               AS On_Time_Orders,
    ROUND(
        100.0 * SUM(CASE WHEN Actual_Delivery_Days
                          <= Expected_Delivery_Days THEN 1
                    ELSE 0 END) / COUNT(*), 1
    )                                                  AS On_Time_Pct
FROM aerospace_supply_chain
GROUP BY Supplier_Location
ORDER BY On_Time_Pct DESC;


-- ─── QUERY 4: High-Risk Orders (delayed AND high defect rate) ─
SELECT
    Order_ID,
    Part_Name,
    Supplier_Location,
    (Actual_Delivery_Days - Expected_Delivery_Days) AS Delay_Days,
    Defect_Rate,
    Shipping_Cost
FROM aerospace_supply_chain
WHERE Actual_Delivery_Days > Expected_Delivery_Days
  AND Defect_Rate > 0.035
ORDER BY Defect_Rate DESC, Delay_Days DESC
LIMIT 20;


-- ─── QUERY 5: Monthly Cost Summary (if order date column added) ─
-- Illustrative — assumes an Order_Date column exists.
-- SELECT
--     DATE_TRUNC('month', Order_Date)  AS Month,
--     SUM(Shipping_Cost)               AS Monthly_Spend,
--     AVG(Defect_Rate)                 AS Avg_Defect,
--     COUNT(*)                         AS Orders
-- FROM aerospace_supply_chain
-- GROUP BY 1
-- ORDER BY 1;
