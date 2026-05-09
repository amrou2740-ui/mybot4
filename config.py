import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PRIMARY_MODEL = "gemini-1.5-flash"
FALLBACK_MODEL = "gemini-1.5-flash"

OUTPUT_DIR = "output"
CACHE_DB = "cache/cache.db"

MAX_RETRIES = 5
RETRY_DELAY = 15
