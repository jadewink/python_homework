# MLB Historical Data Scraper
# This script scrapes historical MLB data from baseball-almanac.com

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MLBHistoricalScraper:
    def __init__(self):
        self.base_url = "https://www.baseball-almanac.com/yearmenu.shtml"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.scraped_urls = set()  # Track scraped URLs to avoid duplication
        self.data = []
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={self.headers['User-Agent']}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {e}")
            return None
    
    def get_year_links(self, start_year=1900, end_year=2024):
        """Get links to individual year pages"""
        driver = self.setup_driver()
        if not driver:
            return []
        
        year_links = []
        try:
            driver.get(self.base_url)
            time.sleep(2)
            
            # Find year links
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                text = link.text.strip()
                
                if href and text.isdigit():
                    year = int(text)
                    if start_year <= year <= end_year:
                        year_links.append((year, href))
            
            logger.info(f"Found {len(year_links)} year links")
            
        except Exception as e:
            logger.error(f"Error getting year links: {e}")
        finally:
            driver.quit()
        
        return sorted(year_links)
    
    def scrape_year_data(self, year, url):
        """Scrape data for a specific year"""
        if url in self.scraped_urls:
            logger.info(f"Already scraped {year}, skipping...")
            return []
        
        driver = self.setup_driver()
        if not driver:
            return []
        
        year_data = []
        try:
            driver.get(url)
            time.sleep(random.uniform(2, 4))  # Random delay to avoid rate limiting
            
            # Look for various data sections
            self._scrape_notable_events(driver, year, year_data)
            self._scrape_statistical_leaders(driver, year, year_data)
            self._scrape_awards_and_achievements(driver, year, year_data)
            
            self.scraped_urls.add(url)
            logger.info(f"Successfully scraped data for {year}")
            
        except Exception as e:
            logger.error(f"Error scraping year {year}: {e}")
        finally:
            driver.quit()
        
        return year_data
    
    def _scrape_notable_events(self, driver, year, year_data):
        """Scrape notable events for the year"""
        try:
            # Look for sections containing notable events
            sections = driver.find_elements(By.TAG_NAME, "p")
            for section in sections:
                text = section.text.strip()
                if len(text) > 50:  # Filter for substantial content
                    year_data.append({
                        'year': year,
                        'category': 'Notable Events',
                        'description': text[:500],  # Limit description length
                        'data_type': 'event'
                    })
        except Exception as e:
            logger.warning(f"Could not scrape notable events for {year}: {e}")
    
    def _scrape_statistical_leaders(self, driver, year, year_data):
        """Scrape statistical leaders for the year"""
        try:
            # Look for tables containing statistics
            tables = driver.find_elements(By.TAG_NAME, "table")
            for table in tables:
                rows = table.find_elements(By.TAG_NAME, "tr")
                if len(rows) > 1:  # Has header and data
                    for row in rows[1:5]:  # Limit to top 5 entries
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) >= 2:
                            year_data.append({
                                'year': year,
                                'category': 'Statistical Leaders',
                                'player_name': cells[0].text.strip() if cells[0].text else 'Unknown',
                                'statistic': cells[1].text.strip() if len(cells) > 1 else '',
                                'value': cells[2].text.strip() if len(cells) > 2 else '',
                                'data_type': 'statistic'
                            })
        except Exception as e:
            logger.warning(f"Could not scrape statistical leaders for {year}: {e}")
    
    def _scrape_awards_and_achievements(self, driver, year, year_data):
        """Scrape awards and achievements for the year"""
        try:
            # Look for award-related content
            elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'MVP') or contains(text(), 'Award') or contains(text(), 'Champion')]")
            for element in elements[:10]:  # Limit results
                text = element.text.strip()
                if text and len(text) > 10:
                    year_data.append({
                        'year': year,
                        'category': 'Awards & Achievements',
                        'description': text[:300],
                        'data_type': 'award'
                    })
        except Exception as e:
            logger.warning(f"Could not scrape awards for {year}: {e}")
    
    def scrape_all_data(self, start_year=1900, end_year=2024, max_years=50):
        """Scrape data for all years within the specified range"""
        year_links = self.get_year_links(start_year, end_year)
        
        # Limit the number of years to scrape to avoid excessive requests
        year_links = year_links[:max_years]
        
        logger.info(f"Starting to scrape {len(year_links)} years of data...")
        
        for i, (year, url) in enumerate(year_links):
            logger.info(f"Scraping {year} ({i+1}/{len(year_links)})")
            year_data = self.scrape_year_data(year, url)
            self.data.extend(year_data)
            
            # Random delay between requests
            time.sleep(random.uniform(3, 6))
            
            # Save intermediate results every 10 years
            if (i + 1) % 10 == 0:
                self.save_to_csv(f"mlb_data_checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        logger.info(f"Completed scraping. Total records: {len(self.data)}")
        return self.data
    
    def save_to_csv(self, filename="mlb_historical_data.csv"):
        """Save scraped data to CSV file"""
        if not self.data:
            logger.warning("No data to save")
            return
        
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        logger.info(f"Data saved to {filename}")
        
        # Print basic statistics
        print(f"\nData Summary:")
        print(f"Total records: {len(df)}")
        print(f"Years covered: {df['year'].min()} - {df['year'].max()}")
        print(f"Categories: {df['category'].unique()}")
        print(f"Data types: {df['data_type'].value_counts()}")

def main():
    """Main function to run the scraper"""
    scraper = MLBHistoricalScraper()
    
    # Scrape data (limiting to recent years for demo)
    scraper.scrape_all_data(start_year=2010, end_year=2024, max_years=15)
    
    # Save to CSV
    scraper.save_to_csv()

if __name__ == "__main__":
    main()