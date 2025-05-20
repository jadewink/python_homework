from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://owasp.org/www-project-top-ten/")

risk_list = []

parent_tag = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/section[1]/ul[2]') 
print(parent_tag)

if (parent_tag):
    children = parent_tag.find_elements(By.TAG_NAME,'a')
    print(children)

    for child in children:
        name = child.find_element(By.TAG_NAME,'strong')
        risk_list.append({
        "title": name.text,
        "link": child.get_attribute('href')
        })

print(risk_list) 
driver.quit()

# Save extracted data to a CSV file
with open('owasp_top_10.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Link"])
    for item in risk_list:
        writer.writerow([item["title"], item["link"]])
