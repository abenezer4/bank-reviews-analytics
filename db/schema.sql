-- Database schema for bank reviews analytics

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    review_date DATE,
    reviewer_name TEXT,
    rating INTEGER,
    title TEXT,
    content TEXT,
    sentiment_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Keywords table
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id INTEGER,
    keyword TEXT NOT NULL,
    frequency INTEGER DEFAULT 1,
    FOREIGN KEY (review_id) REFERENCES reviews(id)
);

-- Themes table
CREATE TABLE IF NOT EXISTS themes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    theme_name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Review-themes mapping table
CREATE TABLE IF NOT EXISTS review_themes (
    review_id INTEGER,
    theme_id INTEGER,
    relevance_score REAL,
    PRIMARY KEY (review_id, theme_id),
    FOREIGN KEY (review_id) REFERENCES reviews(id),
    FOREIGN KEY (theme_id) REFERENCES themes(id)
);

-- Insights table
CREATE TABLE IF NOT EXISTS insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    insight_type TEXT NOT NULL,
    description TEXT,
    confidence_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);