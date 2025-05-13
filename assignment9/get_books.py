# Task 1: Review robots.txt to Ensure Policy Compliance
# Robots.txt references disallowing the /staff/ directory, so that would need to be avoided when scraping

print("Task 2 Understanding HTML and the DOM for the Durham Library Site")
print("Task 3: Write a Program to Extract this Data")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import json
import time
import re 

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://durhamcounty.bibliocommons.com/v2/search?query=learning'%20'spanish&searchType=smart")

# Wait for page to load
time.sleep(5)

# Find the HTML element for a single entry in the search results list.  This is a little tricky.  
# When you select an element in the Chrome developer tools, that part of the web page is highlighted.  
# But, that typically only gets you to the main div.  There is a little arrow next to that div in the developer tools element window, 
# and you click on that to open it up to show the child elements.  Then, you select the element that corresponds to the search results area.  
# Continue in this way, opening up divs or other containers and selecting the one that highlights the area you want.  
# Eventually, you'll get to the first search result.  Hint: You are looking for an li element, because this is an element in an unordered list.  
# Note the values for the class attribute of this entry.  You'll want to save these in some temporary file, as your program will need them.
# # li item class="row cp-search-result-item" for 1 item in result list
# Within that element, find the element that stores the title.  Note the tag type and the class value.  
# # h2 class ="cp-title" contains item title
books = driver.find_elements(By.CLASS_NAME, "cp-search-result-item")
results =[]

for book in books:
    try:
        title_raw = book.find_element(By.CLASS_NAME, "cp-title").text
        title = title_raw.strip().split('\n')[0]
    except:
        title = None
# Within the search results li element, find the element that stores the author.  Hint: This is a link.  
# Note the class value and save it.  Some books do have multiple authors, so you'll have to handle that case.
# # class="author-link" <a> tag contains author's name
    try:
        author_links = book.find_elements(By.CLASS_NAME, "author-link")
        authors = [a.text for a in author_links if a.text.strip()]
    except:
        authors = []

# Within the search results li element, find the element that stores the format of the book and the year it was published.  
# Note the class value and save it.  Now in this case, the class might not be enough to find the part of the li element you want.  
# So look at the div element that contains the format and year.  You want to note that class value too.
# # div class="cp-format-info" 
    try:
        format_info = book.find_element(By.CLASS_NAME, "cp-format-info").text.strip()
        # Typically looks like: "Book - 2021"
        split_parts = format_info.split(" - ")
        book_format = split_parts[0].strip()
        
        
        # Extract year using regex
        year_match = re.search(r"\b(19|20)\d{2}\b", format_info)
        year = year_match.group(0) if year_match else None
    except:
        book_format = None
        year = None

    results.append({
        "title": title,
        "authors": "; ".join(authors), 
        "format": book_format,
        "year": year
    })
#Write to dataframe and print df
df = pd.DataFrame(results)
print(df)

print("Task 4: Write out the Data")
# Save to CSV
df.to_csv("get_books.csv", index=False)

# Save to JSON
with open('get_books.json', 'w') as json_file:
    json.dump(results, json_file, indent=2)

# Close browser
driver.quit()

