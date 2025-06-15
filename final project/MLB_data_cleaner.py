# MLB Data Cleaning and Transformation Module

import pandas as pd
import numpy as np
import re
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MLBDataCleaner:
    def __init__(self, csv_file="mlb_historical_data.csv"):
        self.csv_file = csv_file
        self.raw_data = None
        self.cleaned_data = None
        
    def load_raw_data(self):
        """Load raw data from CSV file"""
        try:
            self.raw_data = pd.read_csv(self.csv_file)
            logger.info(f"Loaded {len(self.raw_data)} records from {self.csv_file}")
            return self.raw_data
        except FileNotFoundError:
            logger.error(f"File {self.csv_file} not found")
            return None
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None
    
    def show_data_quality_report(self):
        """Display data quality report showing before cleaning state"""
        if self.raw_data is None:
            logger.error("No raw data loaded")
            return
        
        print("="*60)
        print("DATA QUALITY REPORT - BEFORE CLEANING")
        print("="*60)
        
        print(f"Total records: {len(self.raw_data)}")
        print(f"Total columns: {len(self.raw_data.columns)}")
        print(f"Memory usage: {self.raw_data.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        print("\nColumn Information:")
        print(self.raw_data.info())
        
        print("\nMissing Values:")
        missing_data = self.raw_data.isnull().sum()
        missing_percent = (missing_data / len(self.raw_data)) * 100
        missing_df = pd.DataFrame({
            'Missing Count': missing_data,
            'Missing Percentage': missing_percent
        })
        print(missing_df[missing_df['Missing Count'] > 0])
        
        print("\nDuplicate Records:")
        duplicates = self.raw_data.duplicated().sum()
        print(f"Total duplicates: {duplicates}")
        
        print("\nData Types:")
        print(self.raw_data.dtypes)
        
        print("\nSample Data:")
        print(self.raw_data.head())
        
        print("\nUnique Values per Column:")
        for col in self.raw_data.columns:
            unique_count = self.raw_data[col].nunique()
            print(f"{col}: {unique_count} unique values")
    
    def clean_data(self):
        """Main data cleaning function"""
        if self.raw_data is None:
            logger.error("No raw data to clean")
            return None
        
        logger.info("Starting data cleaning process...")
        
        # Create a copy to work with
        self.cleaned_data = self.raw_data.copy()
        
        # Step 1: Handle missing values
        self._handle_missing_values()
        
        # Step 2: Remove duplicates
        self._remove_duplicates()
        
        # Step 3: Clean text fields
        self._clean_text_fields()
        
        # Step 4: Standardize categories
        self._standardize_categories()
        
        # Step 5: Extract and clean numerical data
        self._extract_numerical_data()
        
        # Step 6: Create additional features
        self._create_features()
        
        # Step 7: Validate data integrity
        self._validate_data()
        
        logger.info("Data cleaning completed")
        return self.cleaned_data
    
    def _handle_missing_values(self):
        """Handle missing values in the dataset"""
        logger.info("Handling missing values...")
        
        # Fill missing categorical values
        categorical_columns = ['category', 'data_type']
        for col in categorical_columns:
            if col in self.cleaned_data.columns:
                self.cleaned_data[col] = self.cleaned_data[col].fillna('Unknown')
        
        # Fill missing text fields
        text_columns = ['description', 'player_name', 'statistic']
        for col in text_columns:
            if col in self.cleaned_data.columns:
                self.cleaned_data[col] = self.cleaned_data[col].fillna('')
        
        # Fill missing numerical values
        if 'value' in self.cleaned_data.columns:
            self.cleaned_data['value'] = self.cleaned_data['value'].fillna('0')
        
        logger.info("Missing values handled")
    
    def _remove_duplicates(self):
        """Remove duplicate records"""
        initial_count = len(self.cleaned_data)
        
        # Remove exact duplicates
        self.cleaned_data = self.cleaned_data.drop_duplicates()
        
        # Remove duplicates based on key columns
        if all(col in self.cleaned_data.columns for col in ['year', 'category', 'description']):
            self.cleaned_data = self.cleaned_data.drop_duplicates(
                subset=['year', 'category', 'description'], 
                keep='first'
            )
        
        removed_count = initial_count - len(self.cleaned_data)
        logger.info(f"Removed {removed_count} duplicate records")
    
    def _clean_text_fields(self):
        """Clean and standardize text fields"""
        logger.info("Cleaning text fields...")
        
        text_columns = ['description', 'player_name', 'statistic']
        
        for col in text_columns:
            if col in self.cleaned_data.columns:
                # Remove extra whitespace
                self.cleaned_data[col] = self.cleaned_data[col].astype(str).str.strip()
                
                # Remove multiple spaces
                self.cleaned_data[col] = self.cleaned_data[col].str.replace(r'\s+', ' ', regex=True)
                
                # Remove special characters that might cause issues
                self.cleaned_data[col] = self.cleaned_data[col].str.replace(r'[^\w\s\-\.\,\(\)]', '', regex=True)
                
                # Standardize case for player names
                if col == 'player_name':
                    self.cleaned_data[col] = self.cleaned_data[col].str.title()
        
        logger.info("Text fields cleaned")
    
    def _standardize_categories(self):
        """Standardize category values"""
        logger.info("Standardizing categories...")
        
        if 'category' in self.cleaned_data.columns:
            # Standardize category names
            category_mapping = {
                'notable events': 'Notable Events',
                'statistical leaders': 'Statistical Leaders',
                'awards & achievements': 'Awards & Achievements',
                'awards and achievements': 'Awards & Achievements',
                'stats': 'Statistical Leaders',
                'events': 'Notable Events'
            }
            
            self.cleaned_data['category'] = self.cleaned_data['category'].str.lower()
            self.cleaned_data['category'] = self.cleaned_data['category'].replace(category_mapping)
            self.cleaned_data['category'] = self.cleaned_data['category'].str.title()
        
        if 'data_type' in self.cleaned_data.columns:
            # Standardize data types
            type_mapping = {
                'events': 'event',
                'statistics': 'statistic',
                'awards': 'award',
                'stats': 'statistic'
            }
            
            self.cleaned_data['data_type'] = self.cleaned_data['data_type'].str.lower()
            self.cleaned_data['data_type'] = self.cleaned_data['data_type'].replace(type_mapping)
        
        logger.info("Categories standardized")
    
    def _extract_numerical_data(self):
        """Extract and clean numerical data from text fields"""
        logger.info("Extracting numerical data...")
        
        # Extract numerical values from various fields
        if 'value' in self.cleaned_data.columns:
            self.cleaned_data['numeric_value'] = self.cleaned_data['value'].apply(self._extract_number)
        
        # Extract years from descriptions
        if 'description' in self.cleaned_data.columns:
            self.cleaned_data['mentioned_years'] = self.cleaned_data['description'].apply(self._extract_years)
        
        # Create decade column
        if 'year' in self.cleaned_data.columns:
            self.cleaned_data['decade'] = (self.cleaned_data['year'] // 10) * 10
        
        logger.info("Numerical data extracted")
    
    def _extract_number(self, text):
        """Extract numerical value from text"""
        if pd.isna(text) or text == '':
            return 0
        
        # Look for numbers in the text
        numbers = re.findall(r'-?\d+\.?\d*', str(text))
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return 0
        return 0
    
    def _extract_years(self, text):
        """Extract years mentioned in text"""
        if pd.isna(text) or text == '':
            return []
        
        # Look for 4-digit years
        years = re.findall(r'\b(19|20)\d{2}\b', str(text))
        return [int(year) for year in years if year]
    
    def _create_features(self):
        """Create additional features for analysis"""
        logger.info("Creating additional features...")
        
        # Text length features
        if 'description' in self.cleaned_data.columns:
            self.cleaned_data['description_length'] = self.cleaned_data['description'].str.len()
            self.cleaned_data['description_word_count'] = self.cleaned_data['description'].str.split().str.len()
        
        # Era classification
        if 'year' in self.cleaned_data.columns:
            self.cleaned_data['era'] = self.cleaned_data['year'].apply(self._classify_era)
        
        # Record importance score (based on text length and category)
        self.cleaned_data['importance_score'] = self._calculate_importance_score()
        
        logger.info("Additional features created")
    
    def _classify_era(self, year):
        """Classify baseball eras"""
        if year < 1920:
            return 'Dead Ball Era'
        elif year < 1945:
            return 'Live Ball Era'
        elif year < 1960:
            return 'Integration Era'
        elif year < 1976:
            return 'Expansion Era'
        elif year < 1994:
            return 'Free Agency Era'
        elif year < 2006:
            return 'Steroid Era'
        else:
            return 'Modern Era'
    
    def _calculate_importance_score(self):
        """Calculate importance score for records"""
        score = 0
        
        # Base score
        base_score = pd.Series([1] * len(self.cleaned_data))
        
        # Adjust based on category
        if 'category' in self.cleaned_data.columns:
            category_weights = {
                'Awards & Achievements': 3,
                'Statistical Leaders': 2,
                'Notable Events': 1
            }
            category_score = self.cleaned_data['category'].map(category_weights).fillna(1)
            base_score *= category_score
        
        # Adjust based on description length
        if 'description_length' in self.cleaned_data.columns:
            length_score = np.log1p(self.cleaned_data['description_length']) / 10
            base_score *= (1 + length_score)
        
        return base_score
    
    def _validate_data(self):
        """Validate data integrity after cleaning"""
        logger.info("Validating data integrity...")
        
        # Check for required columns
        required_columns = ['year', 'category', 'data_type']
        missing_columns = [col for col in required_columns if col not in self.cleaned_data.columns]
        if missing_columns:
            logger.warning(f"Missing required columns: {missing_columns}")
        
        # Check year range
        if 'year' in self.cleaned_data.columns:
            min_year = self.cleaned_data['year'].min()
            max_year = self.cleaned_data['year'].max()
            if min_year < 1876 or max_year > datetime.now().year:
                logger.warning(f"Unusual year range: {min_year} - {max_year}")
        
        # Check for empty records
        if 'description' in self.cleaned_data.columns:
            empty_descriptions = (self.cleaned_data['description'] == '').sum()
            if empty_descriptions > 0:
                logger.warning(f"Found {empty_descriptions} records with empty descriptions")
        
        logger.info("Data validation completed")
    
    def show_cleaned_data_report(self):
        """Display data quality report after cleaning"""
        if self.cleaned_data is None:
            logger.error("No cleaned data available")
            return
        
        print("="*60)
        print("DATA QUALITY REPORT - AFTER CLEANING")
        print("="*60)
        
        print(f"Total records: {len(self.cleaned_data)}")
        print(f"Total columns: {len(self.cleaned_data.columns)}")
        print(f"Memory usage: {self.cleaned_data.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        print("\nCleaned Data Statistics:")
        print(f"Years covered: {self.cleaned_data['year'].min()} - {self.cleaned_data['year'].max()}")
        print(f"Categories: {self.cleaned_data['category'].value_counts()}")
        
        if 'era' in self.cleaned_data.columns:
            print(f"Eras: {self.cleaned_data['era'].value_counts()}")
        
        print("\nMissing Values (After Cleaning):")
        missing_data = self.cleaned_data.isnull().sum()
        print(missing_data[missing_data > 0])
        
        print("\nSample of Cleaned Data:")
        print(self.cleaned_data.head())
    
    def save_cleaned_data(self, filename="mlb_cleaned_data.csv"):
        """Save cleaned data to CSV"""
        if self.cleaned_data is None:
            logger.error("No cleaned data to save")
            return
        
        self.cleaned_data.to_csv(filename, index=False)
        logger.info(f"Cleaned data saved to {filename}")
    
    def get_analysis_ready_data(self):
        """Return data ready for analysis and visualization"""
        return self.cleaned_data

def main():
    """Main function to demonstrate data cleaning"""
    # Initialize cleaner
    cleaner = MLBDataCleaner()
    
    # Load and analyze raw data
    cleaner.load_raw_data()
    cleaner.show_data_quality_report()
    
    # Clean the data
    cleaned_data = cleaner.clean_data()
    
    # Show results
    cleaner.show_cleaned_data_report()
    
    # Save cleaned data
    cleaner.save_cleaned_data()
    
    return cleaned_data

if __name__ == "__main__":
    main()