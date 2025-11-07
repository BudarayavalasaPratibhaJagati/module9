import os
import psycopg2
from fastapi import FastAPI

app = FastAPI()

def _connect():
    dsn = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/fastapi_db")
    return psycopg2.connect(dsn)

@app.get("/")
def root():
    return {"ok": True, "message": "FastAPI up. Use pgAdmin for SQL screenshots."}

@app.get("/db-ping")
def db_ping():
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                v = cur.fetchone()[0]
        return {"ok": True, "postgres_version": v}
    except Exception as e:
        return {"ok": False, "error": str(e)}
