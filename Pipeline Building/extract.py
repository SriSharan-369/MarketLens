import requests
import logging
import os
from config import *

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_news():
    logging.info("Starting news extraction")
    params ={
        "q": "marketing",
        "apikey": NEWS_API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "articles" not in data:
            raise ValueError("Missing articles field")
        
        logging.info(f"Fetched {len(data['articles'])} articles")
                     
        return data["articles"]

    except requests.exceptions.RequestException as e:
        logging.error(f"API error: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return []