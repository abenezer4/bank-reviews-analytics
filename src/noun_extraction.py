# src/noun_extraction.py

import spacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")

def extract_nouns(text):
    doc = nlp(str(text))
    return [token.text.lower() for token in doc if token.pos_ == "NOUN"]


def compute_noun_counts(df: pd.DataFrame, top_n=50):
    bank_noun_counts = {}

    for bank in df["bank_code"].unique():
        bank_df = df[df["bank_code"] == bank]
        nouns = bank_df["nouns"].explode()
        counts = nouns.value_counts().head(top_n)
        bank_noun_counts[bank] = counts

    return bank_noun_counts
