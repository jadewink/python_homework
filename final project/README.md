# ⚾ MLB Historical Data Dashboard

Jordyn Jones' Python project that scrapes baseball data from the web and displays it in an interactive dashboard. Built as a capstone final project to practice web scraping, data cleaning, and visualization for Python 100.

## What it does

1. **Scrapes baseball data** from baseball-almanac.com using Selenium
2. **Cleans the messy data** and fixes missing values  
3. **Dashboard of charts** in a web dashboard using Streamlit

## Getting started, you'll need:
- Python 3.8 or newer
- Chrome browser

### Install everything:
`pip install streamlit pandas selenium plotly beautifulsoup4 webdriver-manager`

### Run the project:

1. **Get the data** (takes a few minutes):
   `python mlb_web_scraper.py`

2. **Clean the data**:
   `python mlb_data_cleaner.py`

3. **See the dashboard**:
   `streamlit run mlb_data_dashboard.py`

Then open your browser to `http://localhost:8501`

## What you'll see

The dashboard has different tabs:
- **Trends**: Line charts showing how baseball records changed over time
- **Performance**: Heatmaps and top player charts
- **Categories**: Pie charts showing different types of records
- **Details**: Search through all the data

You can filter by year, category, and baseball era using the sidebar controls.

## Files in this project

- `mlb_web_scraper.py` - Gets data from the baseball website
- `mlb_data_cleaner.py` - Fixes and organizes the raw data
- `mlb_data_dashboard.py` - Creates the interactive charts
- `mlb_cleaned_data.csv` - Generated CSV files with the actual data

## Heads up

- The scraper is set to get data from 2010-2017 to be nice to the website
- Sometimes the scraper might break if the website changes
- The dashboard works best with Chrome or Firefox

## If something breaks

- Make sure Chrome is installed and updated
- Inspect with Chrome DevTools
- Try running the scripts one at a time
- Check that all the CSV files got created

---

