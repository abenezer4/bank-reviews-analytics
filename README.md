# Bank Reviews Analytics

## Overview
This project analyzes customer reviews for fintech products to extract insights about customer sentiment, key themes, and product feedback. It scrapes reviews from the Google Play Store, processes the data, performs sentiment analysis, extracts keywords, identifies themes, and generates actionable insights.

## Project Structure
```
.
├── src/
│   ├── main.py
│   ├── scraper.py
│   ├── preprocessing.py
│   ├── sentiment.py
│   ├── keywords.py
│   ├── themes.py
│   ├── insights.py
│   ├── plots.py
│   ├── db_connect.py
│   ├── db_insert.py
├── data/
│   ├── raw/
│   ├── processed/
├── db/
│   ├── schema.sql
├── notebooks/
│   ├── analysis_demo.ipynb
├── reports/
│   ├── figures/
│   ├── final_report.md
├── config.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone this repository:
   ```
   git clone <repository-url>
   cd bank-reviews-analytics
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Configure API keys in `config.py` if needed

4. Run the analysis pipeline:
   ```
   python src/main.py
   ```

## Modules

- **scraper.py**: Scrapes bank reviews from Google Play Store
- **preprocessing.py**: Cleans and prepares review data for analysis
- **sentiment.py**: Performs sentiment analysis on reviews
- **keywords.py**: Extracts important keywords from reviews
- **themes.py**: Identifies common themes in reviews using clustering
- **insights.py**: Generates actionable insights from analyzed data
- **plots.py**: Creates visualizations of the analysis results
- **db_connect.py**: Manages database connections
- **db_insert.py**: Handles insertion of data into the database

## Branch Structure
- `master`: Main branch with stable code
- `task-1`: Data scraping and collection
- `task-2`: Data preprocessing and cleaning
- `task-3`: Sentiment analysis and keyword extraction
- `task-4`: Theme identification and insights generation

## Usage

To run the complete analysis pipeline:
```bash
python src/main.py
```

To experiment with individual components, use the Jupyter notebook:
```bash
jupyter notebook notebooks/analysis_demo.ipynb
```

## License
MIT