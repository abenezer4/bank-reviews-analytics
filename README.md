# Bank Reviews Analytics

## Overview
This project analyzes customer reviews for fintech products to extract insights about customer sentiment, key themes, and product feedback. It scrapes reviews from the Google Play Store, processes the data, performs sentiment analysis, extracts keywords, identifies themes, and generates actionable insights.

## Project Structure
```
.
├── src/
│   ├── 
│   ├── scraper.py
│   ├── preprocessing.py
│   ├── sentiment.py
│   ├── keywords.py
│   ├── themes.py
├── data/
│   ├── raw/
│   ├── processed/
├── db/
├── notebooks/
│   ├── task_1.ipynb
│   ├── task_2.ipynb
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
- **sentiment_analysis.py**: Performs sentiment analysis on reviews
- **tfidfkeywords.py**: Extracts important keywords from reviews
- **themes_builder.py**: Identifies common themes in reviews using clustering

## Branch Structure
- `master`: Main branch with stable code
- `task-1`: Data scraping and Data preprocessing & cleaning
- `task-2`: Sentiment analysis and keyword extraction


## Usage

To run the complete analysis pipeline:
```bash
jupyter notebook notebooks/task_1.ipynb
jupyter notebook notebooks/task_2.ipynb
```

## License
MIT