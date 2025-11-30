# src/tfidf_keywords.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords_per_bank(df: pd.DataFrame, top_n=30):
    keywords_per_bank = {}

    for bank in df["bank_code"].unique():
        subset = df[df["bank_code"] == bank]
        texts = subset["review_text"].fillna("").astype(str).tolist()

        tfidf = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=200
        )
        X = tfidf.fit_transform(texts)

        vocab = tfidf.get_feature_names_out()
        scores = X.mean(axis=0).A1
        
        tfidf_df = pd.DataFrame({"word": vocab, "tfidf": scores})
        tfidf_df = tfidf_df.sort_values("tfidf", ascending=False).head(top_n)

        keywords_per_bank[bank] = tfidf_df["word"].tolist()

    return keywords_per_bank
