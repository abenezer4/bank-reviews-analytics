# src/sentiment_analysis.py

import pandas as pd
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download("vader_lexicon", quiet=True)

sia = SentimentIntensityAnalyzer()

def polarity_to_label(p):
    if p > 0.1:
        return "positive"
    elif p < -0.1:
        return "negative"
    else:
        return "neutral"

def vader_label(c):
    if c >= 0.05:
        return "positive"
    elif c <= -0.05:
        return "negative"
    else:
        return "neutral"


def add_sentiment_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["tb_polarity"] = df["review_text"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    df["tb_subjectivity"] = df["review_text"].apply(lambda x: TextBlob(str(x)).sentiment.subjectivity)
    df["tb_sentiment"] = df["tb_polarity"].apply(polarity_to_label)

    df["vader_compound"] = df["review_text"].apply(
        lambda x: sia.polarity_scores(str(x))["compound"]
    )
    df["vader_sentiment"] = df["vader_compound"].apply(vader_label)

    return df
