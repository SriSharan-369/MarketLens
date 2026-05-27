import requests
import logging 
from config import *

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_news():
    logging.info("Starting news extraction")
    try:
        response = requests.get(BASE_URL, params={"apiKey": NEWS_API_KEY},timeout=10)
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