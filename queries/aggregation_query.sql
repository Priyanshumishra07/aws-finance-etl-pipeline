SELECT
    type,
    SUM(amount) AS total_amount
FROM bank
WHERE year='2024'
AND month='01'
GROUP BY type;