from dotenv import load_dotenv
import os 

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

PROJECT_ID= os.getenv("PROJECT_ID")
DATASET_ID= os.getenv("DATASET_ID")
TABLE_ID= os.getenv("TABLE_ID")

BASE_URL = "https://newsapi.org/v2/everything"

SEARCH_QUERY = "Marketing or AI marketing or Customer Analytics"

PAGE_SIZE= 50
LANGUAGE = "en"  # You can change this to any topic you want to search for

