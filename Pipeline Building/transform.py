import pandas as pd 
from datetime import datetime

positive_words=["growth","innovation","success","increase"]

negative_words=["decline","loss","crisis","failure"]

def get_sentiment(text):
    title = str(title).lower()
    positive_score= sum(word in title for word in positive_words)
    negative_score= sum(word in title for word in negative_words)
    if positive_score > negative_score:
        return "Positive"
    elif negative_score > positive_score:
        return "Negative"
    else:
        return "Neutral"

def transform_data(articles):
    transformed_data = []
    for article in articles:
        title = article.get("title")
        transformed_data.append({
            "source_name": article.get("source", {}).get("name"),
            "author": article.get("author"),
            "title": title,
            "description": article.get("description"),
            "published_at": article.get("publishedAt"),
            "url": article.get("url"),
            "title_length": len(title) if title else 0,
            "sentiment_bucket": get_sentiment(title),
            "ingestion_time": datetime.utcnow()
        })
    df= pd.DataFrame(transformed_data)

    df["published_at"]= pd.to_datetime(df["published_at"], errors="coerce")

    return df

    
