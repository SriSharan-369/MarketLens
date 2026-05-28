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


