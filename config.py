import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

AI_BACKEND_URL = os.getenv("AI_BACKEND_URL", "http://localhost:8080")
APP_BACKEND_PORT = int(os.getenv("APP_BACKEND_PORT", 8000))



# Read Postgres and Redis URLs from environment
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")