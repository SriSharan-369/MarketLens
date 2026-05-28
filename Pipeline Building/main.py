from extract import fetch_news
from transform import transform_articles
from load_bigquery import load_to_bigquery

def run_pipeline():
    articles = fetch_news()
    if not articles:
        print("No articles fetched")
        return
    
    df = transform_articles(articles)
    
    if df.empty:
        print("No transformed data")
        return

    load_to_bigquery(df)
if __name__ == "__main__":
    run_pipeline()