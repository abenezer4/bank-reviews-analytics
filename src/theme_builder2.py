"""
theme_builder.py
----------------
Builds themes per bank using TF-IDF keywords and assigns themes 
to individual reviews based on extracted nouns.

This replaces the static theme approach with a fully data-driven one,
making the theme buckets more accurate and reflective of real user concerns.
"""

# --------------------------------------------------------
# Theme Rule Keywords (Triggers)
# Each list contains indicator terms that define the theme
# --------------------------------------------------------
THEME_RULES = {
    "Performance": [
        "crash", "freeze", "lag", "fail", "slow",
        "error", "loading", "bug", "update", "hang"
    ],
    "Login": [
        "login", "password", "otp", "pin", "authentication",
        "verify", "blocked"
    ],
    "Transactions": [
        "transfer", "payment", "deposit", "withdrawal",
        "balance", "transaction", "card"
    ],
    "UI/UX": [
        "design", "interface", "layout", "menu",
        "navigation", "screen"
    ],
    "Network": [
        "network", "connection", "internet", "coverage"
    ],
    "Customer Support": [
        "service", "support", "help", "response",
        "agent", "center"
    ]
}


# --------------------------------------------------------
# Function: Build dynamic theme dictionary per bank
# --------------------------------------------------------
def build_themes_from_tfidf(keywords_per_bank, theme_rules=THEME_RULES):
    """
    Builds a theme dictionary per bank using TF-IDF keywords.

    Parameters:
        keywords_per_bank (dict):
            {
                "CBE": [... list of keywords ...],
                "Abyssinia": [...],
                "DashenBank": [...]
            }
        theme_rules (dict): theme keywords used for classification.

    Returns:
        dict:
            {
                "CBE": {
                    "Performance": [...keywords...],
                    "Login": [...],
                    ...
                    "Other": [...]
                },
                ...
            }
    """
    bank_themes = {}

    for bank, keywords in keywords_per_bank.items():
        themes = {theme: [] for theme in theme_rules.keys()}
        themes["Other"] = []

        for kw in keywords:
            kw_lower = kw.lower()
            assigned = False

            # classify keyword based on trigger rules
            for theme_name, triggers in theme_rules.items():
                # if any trigger appears inside the TF-IDF keyword string
                if any(trigger in kw_lower for trigger in triggers):
                    themes[theme_name].append(kw_lower)
                    assigned = True
                    break

            # if unmatched, push to "Other"
            if not assigned:
                themes["Other"].append(kw_lower)

        bank_themes[bank] = themes

    return bank_themes


# --------------------------------------------------------
# Helper: Match nouns to theme keywords more flexibly
# --------------------------------------------------------
def _noun_matches_theme(noun, theme_keywords):
    noun = noun.lower()

    for kw in theme_keywords:
        kw = kw.lower()
        if kw == noun:
            return True
        if kw in noun or noun in kw:
            return True
    return False


# --------------------------------------------------------
# Function: Assign theme per review using dynamic bank themes
# --------------------------------------------------------
def assign_theme_tfidf(row, bank_themes):
    """
    Assign a theme to the review based on review nouns and
    the TF-IDF derived theme dictionary for the bank.

    Parameters:
        row (pandas.Series):
            Contains bank_code and nouns list.
        bank_themes (dict):
            Output of build_themes_from_tfidf()

    Returns:
        str: the theme name assigned to the review
    """
    bank = row["bank_code"]
    nouns = row["nouns"]

    themes_for_bank = bank_themes.get(bank, {})

    # Try matching nouns against theme keywords
    for theme_name, keywords in themes_for_bank.items():
        if theme_name == "Other":
            continue
        if any(_noun_matches_theme(noun, keywords) for noun in nouns):
            return theme_name

    return "Other"
