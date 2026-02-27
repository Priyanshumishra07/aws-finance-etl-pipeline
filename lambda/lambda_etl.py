import json
import boto3
import csv
import hashlib
from io import StringIO
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    if "raw/" not in key:
        return
    
    print("Processing file:", key)

    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')

    reader = csv.DictReader(StringIO(content))

    cleaned_rows = []
    error_rows = []
    seen_hashes = set()

    for row in reader:
        try:
            # Extract date
            date_obj = datetime.strptime(row['date'], "%Y-%m-%d")
            year = str(date_obj.year)
            month = f"{date_obj.month:02d}"

            amount = float(row['amount'])

            # Deduplication using hash
            row_hash = hashlib.md5(str(row).encode()).hexdigest()
            if row_hash in seen_hashes:
                continue
            seen_hashes.add(row_hash)

            # Business logic
            signed_amount = amount if row['type'] == "Credit" else -amount

            transaction_flag = "High Value" if amount > 50000 else "Normal"

            cleaned_rows.append([
                row['transaction_id'],
                row['date'],
                amount,
                signed_amount,
                row['type'].upper(),
                row['account_id'],
                row['merchant'],
                row['category'],
                transaction_flag
            ])

        except Exception as e:
            print("Row error:", e)
            error_rows.append(row)

    # Write cleaned CSV WITHOUT year/month columns
    output_buffer = StringIO()
    writer = csv.writer(output_buffer)

    writer.writerow([
        "transaction_id",
        "date",
        "amount",
        "signed_amount",
        "type",
        "account_id",
        "merchant",
        "category",
        "transaction_flag"
    ])

    writer.writerows(cleaned_rows)

    # Use last detected year/month (safe since single file upload)
    processed_key = f"processed/bank/year={year}/month={month}/bank_transactions_cleaned.csv"

    s3.put_object(
        Bucket=bucket,
        Key=processed_key,
        Body=output_buffer.getvalue()
    )

    # Write errors
    if error_rows:
        error_buffer = StringIO()
        writer = csv.DictWriter(error_buffer, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(error_rows)

        s3.put_object(
            Bucket=bucket,
            Key="error/bank/bank_transactions_error.csv",
            Body=error_buffer.getvalue()
        )

    return {
        'statusCode': 200,
        'body': json.dumps("ETL Completed Successfully")
    }