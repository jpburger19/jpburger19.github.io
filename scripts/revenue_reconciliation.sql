-- Purpose: Reconcile Gross Transaction Volume (GTV) against Net Revenue
-- Calculates Interchange, Markup, and Partner Commission splits.

WITH transaction_summary AS (
    SELECT 
        partner_id,
        merchant_category,
        SUM(transaction_amount) AS total_gtv,
        COUNT(transaction_id) AS tx_count,
        -- Interchange varies by category (e.g., Retail vs. E-commerce)
        CASE 
            WHEN merchant_category = 'E-commerce' THEN 0.023
            ELSE 0.019 
        END AS interchange_rate
    FROM `fintech-platform.payments.processed_tx`
    WHERE status = 'Success'
    GROUP BY 1, 2
)
SELECT 
    partner_id,
    total_gtv,
    (total_gtv * interchange_rate) AS interchange_cost,
    (total_gtv * 0.005) AS platform_markup, -- Standard 50bps markup
    ((total_gtv * 0.005) * 0.5) AS partner_commission -- 50/50 Revenue Share
FROM transaction_summary;