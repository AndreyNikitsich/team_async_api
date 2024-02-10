import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_DSL = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", 5432),
    "options": "-c search_path=content",
}

STATE_FILE_PATH = os.getenv("STATE_FILE_PATH", "../state.json")

ELASTICSEARCH_DSL = {
    "hosts": [os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")],
}

BATCH_SIZE = int(os.getenv("BATCH_SIZE", 100))

SLEEP_TIME = int(os.getenv("SLEEP_TIME", 10))
