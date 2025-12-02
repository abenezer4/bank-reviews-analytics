import pandas as pd
from sqlalchemy import text
from db_connection import get_engine
import json


def load_data_to_db(csv_path="processed_reviews.csv"):
    print(f"Loading data from {csv_path} into PostgreSQL database...")
    df = pd.read_csv(csv_path)

    engine = get_engine()

    # Insert banks first
    banks = (
        df[["bank_code", "bank_name"]]
        .drop_duplicates()
        .to_dict(orient="records")
    )

    with engine.begin() as conn:
        for b in banks:
            conn.execute(
                text("""
                    INSERT INTO banks (bank_code, bank_name)
                    VALUES (:bank_code, :bank_name)
                    ON CONFLICT (bank_code) DO NOTHING
                """),
                b
            )

        # Fetch bank map after insert
        id_map = {
            r.bank_code: r.bank_id
            for r in conn.execute(text("SELECT bank_id, bank_code FROM banks"))
        }

        # Insert reviews
        for _, r in df.iterrows():
            payload = {
                "review_id": r["review_id"],
                "review_text": r.get("review_text"),
                "clean_text": r.get("clean_text"),
                "tokens": json.dumps(r.get("tokens")) if r.get("tokens") is not None else None,
                "rating": int(r["rating"]),
                "vader_sentiment": r.get("vader_sentiment"),
                "tb_sentiment": r.get("tb_sentiment"),
                "vader_compound": r.get("vader_compound"),
                "tb_polarity": r.get("tb_polarity"),
                "theme": r.get("theme"),
                "review_date": r.get("review_date"),
                "bank_id": id_map.get(r["bank_code"])
            }

            conn.execute(
                text("""
                    INSERT INTO reviews (
                        review_id, review_text, clean_text, tokens,
                        rating, vader_sentiment, tb_sentiment, vader_compound,
                        tb_polarity, theme, review_date, bank_id
                    )
                    VALUES (
                        :review_id, :review_text, :clean_text, :tokens,
                        :rating, :vader_sentiment, :tb_sentiment, :vader_compound,
                        :tb_polarity, :theme, :review_date, :bank_id
                    )
                    ON CONFLICT (review_id) DO NOTHING
                """),
                payload
            )

    print("Data successfully loaded into PostgreSQL!")
