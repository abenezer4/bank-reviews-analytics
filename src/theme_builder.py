

import re
import pandas as pd

performance_words = ["app", "crash", "crashing", "update", "freeze", "lag", "bug", "speed", "slow"]
login_words = ["login", "password", "otp", "pin", "authentication"]
transaction_words = ["transfer", "payment", "balance", "deposit", "withdrawal", "transaction"]
uiux_words = ["design", "interface", "layout", "navigation", "button"]
network_words = ["network", "internet", "connection"]
support_words = ["service", "support", "help", "response", "agent"]


def build_themes_per_bank(noun_counts_by_bank: dict):
    bank_themes = {}

    for bank, noun_counts in noun_counts_by_bank.items():
        themes = {
            "Performance": [],
            "Login Issues": [],
            "Transactions": [],
            "UI/UX": [],
            "Network": [],
            "Customer Support": [],
            "Other": []
        }

        for noun in noun_counts.index:
            if noun in performance_words:
                themes["Performance"].append(noun)
            elif noun in login_words:
                themes["Login Issues"].append(noun)
            elif noun in transaction_words:
                themes["Transactions"].append(noun)
            elif noun in uiux_words:
                themes["UI/UX"].append(noun)
            elif noun in network_words:
                themes["Network"].append(noun)
            elif noun in support_words:
                themes["Customer Support"].append(noun)
            else:
                themes["Other"].append(noun)

        bank_themes[bank] = themes

    return bank_themes



def assign_theme(bank_code, nouns, bank_themes):
    nouns = set(nouns)
    themes = bank_themes[bank_code]

    for theme_name, word_list in themes.items():
        for w in word_list:
            if w in nouns:
                return theme_name
    return "Other"
