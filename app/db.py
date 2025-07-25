# app/db.py
import psycopg2
import os

POSTGRES_URL = os.getenv("POSTGRES_URL")

def save_review_result(review_id, pr_url, review_text):
    conn = psycopg2.connect(POSTGRES_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS review_results (
            id UUID PRIMARY KEY,
            pr_url TEXT,
            review_text TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("INSERT INTO review_results (id, pr_url, review_text) VALUES (%s, %s, %s)",
                (review_id, pr_url, review_text))
    conn.commit()
    cur.close()
    conn.close()

def get_review_result(review_id):
    conn = psycopg2.connect(POSTGRES_URL)
    cur = conn.cursor()
    cur.execute("SELECT review_text FROM review_results WHERE id=%s", (review_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/potpie"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/potpie"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
