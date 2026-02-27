📌 Overview

This project implements a production-style serverless ETL pipeline for processing financial transaction data using AWS services.

The pipeline ingests raw banking data, applies transformation and validation logic, partitions processed data for analytics optimization, and enables SQL-based querying using Amazon Athena.

🏗 Architecture

S3 (Raw Layer)
→ AWS Lambda (ETL Processing)
→ S3 (Processed Layer - Partitioned)
→ AWS Glue (Metadata Catalog)
→ Amazon Athena (Query Layer)

⚙ Technologies Used

AWS S3

AWS Lambda (Python 3.10)

AWS Glue Crawler

Amazon Athena

CloudWatch Logs

IAM Roles

🔄 Data Flow

Raw CSV uploaded to raw/bank/

Lambda triggered automatically

Data validation & deduplication applied

Business logic transformations:

Signed transaction amounts

High-value transaction flag

Processed data stored in:

processed/bank/year=YYYY/month=MM/

Glue crawler updates metadata

Athena queries enable analytics

🚀 Key Features

Event-driven architecture

Partitioned S3 data lake

Schema normalization

Deduplication logic

Error quarantine layer

Partition pruning optimization

Serverless compute model

Cost-efficient analytics

📊 Sample Queries

See /queries folder for SQL examples.

💰 Cost Optimization Strategy

Used serverless Lambda (no idle compute)

Partitioned S3 data to reduce Athena scanned data

On-demand Glue crawler

Minimized data storage footprint

📈 Future Improvements

Migrate ETL to AWS Glue Spark for large-scale processing

Add infrastructure-as-code using Terraform

Add CI/CD pipeline

Implement data quality validation framework
