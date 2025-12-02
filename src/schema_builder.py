from sqlalchemy import text
from db_connection import get_engine

def create_tables():
    engine = get_engine()

    create_banks = """
    CREATE TABLE IF NOT EXISTS banks (
        bank_id SERIAL PRIMARY KEY,
        bank_code VARCHAR(20) UNIQUE,
        bank_name VARCHAR(100)
    );
    """

    create_reviews = """
    CREATE TABLE IF NOT EXISTS reviews (
        review_id VARCHAR PRIMARY KEY,
        review_text TEXT,
        clean_text TEXT,
        tokens JSONB,
        rating INT,
        vader_sentiment VARCHAR(20),
        tb_sentiment VARCHAR(20),
        vader_compound FLOAT,
        tb_polarity FLOAT,
        theme VARCHAR(50),
        review_date TIMESTAMP,
        bank_id INT REFERENCES banks(bank_id)
    );
    """

    with engine.begin() as conn:
        conn.execute(text(create_banks))
        conn.execute(text(create_reviews))

    print("Tables created successfully.")
