CREATE OR REPLACE VIEW monthly_summary AS
SELECT
    year,
    month,
    SUM(amount) AS total_amount,
    SUM(CASE WHEN type='DEBIT' THEN amount ELSE 0 END) AS total_debit,
    SUM(CASE WHEN type='CREDIT' THEN amount ELSE 0 END) AS total_credit
FROM bank
GROUP BY year, month;