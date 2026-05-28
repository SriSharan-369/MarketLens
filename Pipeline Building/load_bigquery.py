from google.cloud import bigquery
from config import *

client = bigquery.Client(project=PROJECT_ID)
def load_to_bigquery(df):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND"
    )
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # Wait for the job to complete
    print(f"Loaded {job.output_rows} rows into {table_id}.")