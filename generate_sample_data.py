import csv
import random
from datetime import datetime, timedelta

output_file = "bank_transactions_1000.csv"

merchants = ["Amazon", "Flipkart", "Apple", "Uber", "Swiggy", "Salary", "Bonus", "Zara", "Nike", "Walmart"]
categories = ["Shopping", "Electronics", "Travel", "Food", "Income"]
types = ["Debit", "Credit"]
statuses = ["Success", "Success", "Success", "Success", "Failed"]  # 80% success

start_date = datetime(2024, 1, 1)

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Header
    writer.writerow([
        "transaction_id",
        "date",
        "amount",
        "type",
        "account_id",
        "merchant",
        "category",
        "status"
    ])

    for i in range(1, 1001):
        txn_id = f"TXN{i:04d}"

        random_days = random.randint(0, 90)
        date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

        amount = random.randint(100, 100000)
        txn_type = random.choice(types)
        account_id = f"ACC{random.randint(100, 999)}"
        merchant = random.choice(merchants)
        category = random.choice(categories)
        status = random.choice(statuses)

        writer.writerow([
            txn_id,
            date,
            amount,
            txn_type,
            account_id,
            merchant,
            category,
            status
        ])

print("1000-row sample dataset generated successfully!")