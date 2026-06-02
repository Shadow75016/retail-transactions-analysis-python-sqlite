-- 1. Chiffre d'affaires total
SELECT ROUND(SUM(line_revenue), 2) AS total_revenue
FROM transactions_clean;

-- 2. Nombre de factures
SELECT COUNT(DISTINCT invoice_no) AS total_invoices
FROM transactions_clean;

-- 3. Ventes par pays
SELECT country, ROUND(SUM(line_revenue), 2) AS revenue
FROM transactions_clean
GROUP BY country
ORDER BY revenue DESC
LIMIT 10;

-- 4. Top 10 produits par revenu
SELECT description, ROUND(SUM(line_revenue), 2) AS revenue
FROM transactions_clean
GROUP BY description
ORDER BY revenue DESC
LIMIT 10;

-- 5. Top 10 clients par revenu
SELECT customer_id, ROUND(SUM(line_revenue), 2) AS revenue
FROM transactions_clean
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY revenue DESC
LIMIT 10;

-- 6. Ventes mensuelles
SELECT invoice_year_month, ROUND(SUM(line_revenue), 2) AS revenue
FROM transactions_clean
GROUP BY invoice_year_month
ORDER BY invoice_year_month;

-- 7. Panier moyen par facture
SELECT ROUND(AVG(invoice_total), 2) AS average_basket
FROM (
    SELECT invoice_no, SUM(line_revenue) AS invoice_total
    FROM transactions_clean
    GROUP BY invoice_no
) t;

-- 8. Nombre d'annulations
SELECT COUNT(DISTINCT invoice_no) AS cancelled_invoices
FROM cancellations;

-- 9. Part des annulations (en nombre de factures)
SELECT
    ROUND(
        100.0 * (
            SELECT COUNT(DISTINCT invoice_no) FROM cancellations
        ) /
        (
            (SELECT COUNT(DISTINCT invoice_no) FROM transactions_clean) +
            (SELECT COUNT(DISTINCT invoice_no) FROM cancellations)
        ),
        2
    ) AS cancellation_rate_pct;

-- 10. Top pays par nombre de factures
SELECT country, COUNT(DISTINCT invoice_no) AS invoice_count
FROM transactions_clean
GROUP BY country
ORDER BY invoice_count DESC
LIMIT 10;

-- 11. Top 10 produits par revenu (hors lignes non produit)
SELECT description, ROUND(SUM(line_revenue), 2) AS revenue
FROM transactions_clean
WHERE description IS NOT NULL
  AND TRIM(description) <> ''
  AND UPPER(description) NOT IN ('MANUAL', 'POSTAGE', 'DOTCOM POSTAGE')
GROUP BY description
ORDER BY revenue DESC
LIMIT 10;

-- 12. Part des ventes sans customer_id
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN customer_id IS NULL OR customer_id = '' THEN line_revenue ELSE 0 END)
        / SUM(line_revenue),
        2
    ) AS revenue_without_customer_pct
FROM transactions_clean;

-- 13. Part du Royaume-Uni dans le chiffre d'affaires
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN country = 'United Kingdom' THEN line_revenue ELSE 0 END)
        / SUM(line_revenue),
        2
    ) AS uk_revenue_share_pct
FROM transactions_clean;