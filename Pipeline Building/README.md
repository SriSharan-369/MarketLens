## Pipeline Building 

## Marketlens pipeline overview 
An end to end Python ETL pipeline that fetches marketing related news articles from NewsAPI, cleans and enriches the data, and loads it into Google BigQuery for analytics.

Each pipeline run:
1. Extracts up to 100 articles matching a configurable search query from NewsAPI
2. Transforms the raw JSON into a clean tabular format with derived fields (title length, sentiment bucket, ingestion timestamp)
3. Loads the results into BigQuery using a batch load job [ compatible with the free Bigquery Sandbox ]

## Data Flow 

```
NewsAPI
   ↓
Python Extraction Layer
   ↓
Transformation & Enrichment
   ↓
BigQuery
   ↓
SQL Insights Query
```
## Architecture 

### Architecture Diagram 

<p align="left">
  <img src="./MarketLens PipeLine.jpeg">
</p>

### Data pipeline Architecture 
```
┌─────────────┐     ┌──────────────┐     ┌───────────────────────┐
│  NewsAPI    │────▶│  extract.py  │────▶│    transform.py       │
│ /v2/every-  │     │              │     │                       │
│    thing    │     │ • HTTP call  │     │ • Flatten nested JSON │
└─────────────┘     │ • Error hand.│     │ • Coerce timestamps   │
                    │ • Retry log. │     │ • Fill nulls          │
                    └──────────────┘     │ • Derive fields       │
                                         └───────────┬───────────┘
                                                     │
                                         ┌───────────▼───────────┐
                                         │  load_bigquery.py     │
                                         │                       │
                                         │ • Batch load          │
                                         │ • WRITE_APPEND        │
                                         │ • Auto-create table   │
                                         └───────────┬───────────┘
                                                     │
                                         ┌───────────▼───────────┐
                                         │  BigQuery             │
                                         │  marketlens_data      │
                                         │  .news_articles       │
                                         └───────────────────────┘
```
## Folder Structure 
```
marketlens/
│
├── pipeline building/
│   ├── extract.py         # Extraction layer — calls NewsAPI
│   ├── transform.py       # Transformation layer — cleans and enriches data
│   ├── load_bigquery.py   # Loading layer — writes to BigQuery
│   └── main.py            # Pipeline entry point / orchestrator
│
├── sql/
│   └── trending_topics.sql  # Analytical queries for the loaded data
│
├── logs/                  # Pipeline log files (created on first run)
│
├── config.py              # Centralised, parameterised configuration
├── requirements.txt       # Python dependencies
├── .env          # Template for required environment variables
├── .gitignore
│
├── product scoping/
│   ├── README.md    
└── README.md
```
## Setup Instructions 

1. Clone / download the project

```
git clone <your-repository-url>
cd pipeline_building
```

2. Create a Python virtual environment

Windows
```
python -m venv venv
venv\Scripts\activate
```
Mac/Linux
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```
pip install -r requiremnts.txt
```

## 4. Configure environment variables

Create a .env file:

```
NEWS_API_KEY=your_newsapi_key
PROJECT_ID=your_bigquery_project_id
DATASET_ID=marketlens_demo
TABLE_ID=news_articles
```
## 5. BigQuery Setup

This project uses Google BigQuery Sandbox, which is available for free without a billing account.

Steps
1. Open BigQuery Console
2. Create a GCP project
3. Create dataset:
```
marketlens_data
```
## 6. Authenticate locally:
```
gcloud auth application-default login
```

## 7. Running the Pipeline

Run the complete ETL pipeline:
```
python pipeline_building/main.py
```

Successful execution loads transformed data into:
```
PROJECT_ID.marketlens_data.news_articles
```

## 8. Transformation Logic 

The transformation layer performs the following operations:

1. Flatten Nested JSON

Extracts nested fields such as:
```
source.name
```

into tabular columns:
```
source_name
```
2. Handle Nulls and Type Conversion
   
- Missing titles handled safely
- Invalid timestamps coerced using pandas.to_datetime()
- Empty values handled with default logic

3. Derived Analytical Fields
   
title_length: Calculates the length of each article headline.

sentiment_bucket: Classifies headlines into:

- Positive
- Negative
- Neutral

based on keyword matching logic.

ingestion_time: Captures pipeline ingestion timestamp for auditability.

## 9. BigQuery Schema

```
Field Name	Data Type
source_name	STRING
author	STRING
title	STRING
description	STRING
published_at	TIMESTAMP
url	STRING
title_length	INTEGER
sentiment_bucket	STRING
ingestion_time	TIMESTAMP
```
## 10. Sample SQL Query

```
SELECT
    source_name,
    sentiment_bucket,
    COUNT(*) AS total_articles
FROM `your_project.marketlens_demo.news_articles`
GROUP BY source_name, sentiment_bucket
ORDER BY total_articles DESC;
```

This query shows which news sources publish the most positive, negative, or neutral marketing-related articles.

## 11. Logging and Error Handling 

The pipeline includes:

- API exception handling
- HTTP error handling
- Logging to logs/pipeline.log
- Graceful failure handling for invalid responses

## How you would run in this in Production 

1. How would you schedule this pipeline to run automatically?

Currently, the pipeline is executed manually using:
```
python pipeline_building/main.py
```
In a real production environment, manual execution is not practical because data pipelines usually need to run repeatedly and reliably without human intervention.

To automate execution, the pipeline can be scheduled using orchestration or scheduling tools such as:
```
Apache Airflow
Google Cloud Composer
Cron Jobs (Linux)
Windows Task Scheduler
```
Example :

If the business wants fresh marketing news every morning, the scheduler could run the pipeline automatically every day at 8 AM.
The scheduler will simply trigger:
```
python pipeline-building/main.py
```
at the configured interval.

Why scheduling matters ?

Automation provides several operational benefits:

- Removes manual effort
- Ensures consistent data updates
- Reduces human error
- Makes reporting and analytics more reliable
- Enables pipelines to run continuously in production

Why Airflow is commonly used ?

Apache Airflow is widely used in data engineering because it provides:

- Workflow orchestration
- Dependency management
- Retry handling
- Monitoring dashboards
- Scheduling support
- Failure notifications

In a larger system, Airflow would manage this ETL pipeline as a DAG (Directed Acyclic Graph).

## How would you know if it failed?

Failures are captured using Python logging and exception handling.

1. Alerting

Automatic notifications can be sent through:

- Email
- Slack
- Microsoft Teams

Example: “MarketLens pipeline failed at 08:00 AM during BigQuery load stage.”
This helps engineers respond quickly.

2. Retry Mechanisms

Temporary failures such as network timeouts should not immediately fail the entire pipeline.

Retries can be added for:

- API requests
- BigQuery operations

This improves reliability.

3. Logging

Instead of local log files, logs can be sent to platforms such as:

- Google Cloud Logging
- ELK Stack
- Datadog

This makes debugging easier in distributed systems.

4. Data Quality Validation

The pipeline should also validate the data itself.

Examples:
- Check if row count suddenly drops
- Validate null percentages
- Detect duplicate articles
- Ensure timestamps are valid

This helps detect silent data issues even when the pipeline technically succeeds.

## What would you add or change if this pipeline needed to scale to 10x the data volume?

The current implementation works well for small-to-medium datasets, but larger data volumes will require architectural improvements.

Improvements for Large-Scale Processing
1. Replace Pandas with Apache Spark

Pandas loads everything into memory on one machine.

For large-scale workloads, Apache Spark will be better because it supports:

- distributed processing
- parallel execution
- cluster-based computation

This allows the pipeline to process significantly larger datasets efficiently.

2. Incremental Ingestion

Currently, every run fetches the latest articles again.
At large scale, repeatedly processing old data wastes resources.
A better design is to track the latest processed timestamp and ingest only new articles

Benefits:

- faster pipeline execution
- reduced API calls
- lower storage costs
  
3. BigQuery Partitioned Tables

Large tables become slower and more expensive to query.
Partitioning the table by "published_at" will improve query performance, storage efficiency, cost optimization

Example:
Queries for one specific day would scan only that partition instead of the entire table.

4. Deduplication Logic

News APIs often return repeated articles.At larger scale, duplicates become a major issue.

The pipeline can implement:
```
df.drop_duplicates(subset=["title"])
```
or deduplicate using article URLs or hashes.

This improves data quality and reduces unnecessary storage.

5. Workflow Orchestration with Airflow

As pipelines grow, multiple stages and dependencies appear.

Airflow will help to manage:

- scheduling
- retries
- monitoring
- dependency execution
- pipeline visibility

This is a standard practice in modern data engineering.


