from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import redis
import requests
import psycopg2
from config import AI_BACKEND_URL, POSTGRES_URL, REDIS_URL

app = FastAPI()

# CORS configuration
origins = [
     "http://localhost:3000",
    "http://127.0.0.1:3000",  # include 127.0.0.1
    "http://localhost:3001",
    "http://127.0.0.1:3001",  # include 127.0.0.1
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allow requests from these origins
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"],         # allow all headers
)

# SQLite DB connection
def check_db():
    try:
        conn = psycopg2.connect(POSTGRES_URL)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name TEXT);")
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Postgres Error:", e)
        return False


# Redis connection
def check_redis():
    try:
        # Connect using the Redis URL
        r = redis.Redis.from_url(REDIS_URL)
        r.ping()
        return True
    except Exception as e:
        print("Redis Error:", e)
        return False
@app.get("/")
def status():
    # Check AI backend connectivity
    try:
        res = requests.get(f'{AI_BACKEND_URL}/connect', timeout=2).json()
        print(res)
        ai_to_backend_connection = res['ai_to_backend_connection'] if 'ai_to_backend_connection' in res else False
    except Exception as e:
        print("AI Connection Error:", e)
        ai_to_backend_connection = False

    return {
        "app": "backend",
        "db_connected": check_db(),
        "redis_connected": check_redis(),
        "ai_to_backend_connection": ai_to_backend_connection
    }

@app.get("/connect")
def connect():
    # Return True so AI backend can confirm connectivity
    return {"backend_to_ai_connection": True}
