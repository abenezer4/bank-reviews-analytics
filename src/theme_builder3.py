"""
theme_builder_advanced.py

Data-driven theme extraction using:
- Negative-review TF-IDF keywords
- Expanded TF-IDF tokens
- Regex trigger patterns
- Clean text token matching

Outputs:
1) bank_themes: structured theme lexicon per bank
2) assign_theme(): assigns theme to each review
"""

import re
import pandas as pd
# ------------------------------------------------------------
# 1) Theme trigger PHRASE patterns (strong match)
# (real banking complaints)
# ------------------------------------------------------------
PHRASE_PATTERNS = {
    "Login": [
        r"otp", r"pin", r"login", r"authentication", r"password",
        r"invalid", r"blocked", r"verification"
    ],
    "Network": [
        r"no network", r"weak network", r"connection",
        r"network unavailable", r"internet", r"sim"
    ],
    "Transactions": [
        r"transfer", r"payment", r"withdraw", r"deposit",
        r"balance", r"transaction failed", r"card", r"statement"
    ],
    "Performance": [
        r"crash", r"freez", r"slow", r"lag", r"hang",
        r"timeout", r"loading", r"unresponsive", r"update"
    ],
    "Customer Support": [
        r"service unavailable", r"customer service",
        r"support", r"response", r"call center"
    ],
    "UI/UX": [
        r"interface", r"design", r"layout", r"navigation",
        r"menu", r"button", r"screen"
    ]
}

# generic fallback terms — if found, weaker signal
WEAK_TERMS = [
    "problem", "issue", "error", "bad", "poor", "not working"
]


# ------------------------------------------------------------
# 2) Expand TF-IDF keywords into unigrams & bigrams
# ------------------------------------------------------------
def expand_keywords(keywords):
    """
    Takes TF-IDF keyword list and expands them into:
    - original words/phrases
    - individual tokens from phrases

    Returns a big list for flexible matching
    """
    expanded = set()

    for kw in keywords:
        kw = kw.lower().strip()
        expanded.add(kw)

        # split multi-word tfidf keys
        parts = kw.split()
        for p in parts:
            if len(p) > 2:       # drop tiny tokens
                expanded.add(p)

    return list(expanded)


# ------------------------------------------------------------
# 3) Build data-driven theme dictionary per bank
# Using NEGATIVE reviews ONLY
# ------------------------------------------------------------
def build_bank_themes(df, extract_keywords_func, top_n=50):
    """
    df must contain:
    - vader_sentiment (negative/positive/neutral)
    - bank_code
    - clean_text

    extract_keywords_func:
        function returning tfidf keywords per bank
    """
    negative = df[df["vader_sentiment"] == "negative"]
    keyword_sets = extract_keywords_func(negative, top_n=top_n)

    bank_themes = {}

    for bank, kws in keyword_sets.items():
        expanded = expand_keywords(kws)

        bank_themes[bank] = {
            "keywords": expanded,
            "themes": {
                theme: [] for theme in PHRASE_PATTERNS.keys()
            }
        }

        # assign TF-IDF keywords to buckets by phrase match
        for kw in expanded:
            placed = False
            for theme, patterns in PHRASE_PATTERNS.items():
                if any(re.search(p, kw) for p in patterns):
                    bank_themes[bank]["themes"][theme].append(kw)
                    placed = True
                    break

            if not placed:
                # accents generic
                for g in WEAK_TERMS:
                    if g in kw:
                        bank_themes[bank]["themes"].setdefault("GenericIssues", [])
                        bank_themes[bank]["themes"]["GenericIssues"].append(kw)
                        placed = True
                        break

            if not placed:
                bank_themes[bank]["themes"].setdefault("Other", [])
                bank_themes[bank]["themes"]["Other"].append(kw)

    return bank_themes


# ------------------------------------------------------------
# 4) Scoring function
# The theme with MOST hits wins
# ------------------------------------------------------------
def score_theme(clean_text, themes):
    scores = {t: 0 for t in themes.keys()}

    for theme, words in themes.items():
        for w in words:
            if w in clean_text:
                scores[theme] += 2  # high weight if full TFIDF kw hit

        # phrase triggers add extra weight
        if theme in PHRASE_PATTERNS:
            for pattern in PHRASE_PATTERNS[theme]:
                if re.search(pattern, clean_text):
                    scores[theme] += 3

    # weak generic words count low
    for w in WEAK_TERMS:
        if w in clean_text:
            scores["GenericIssues"] = scores.get("GenericIssues", 0) + 1

    # return theme with best score
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "Other"  # no signals found

    return best


# ------------------------------------------------------------
# 5) Assign final theme to each review
# ------------------------------------------------------------
def assign_theme(row, bank_themes):
    bank = row["bank_code"]

    # Safety handling for missing clean_text
    clean_text = row.get("clean_text", "")

    if not isinstance(clean_text, str):
        if pd.isna(clean_text):
            clean_text = ""
        else:
            clean_text = str(clean_text)

    clean_text = clean_text.lower()

    if bank not in bank_themes:
        return "Other"

    themes = bank_themes[bank]["themes"]
    return score_theme(clean_text, themes)