from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import csv

file = open("scraped_data.csv", "w", newline='')
writer = csv.writer(file)
writer.writerow(["ID", "Name", "Price", "Specifications", "Number_Of_Reviews"])

browser_driver = Service(
    ".\chromedriver.exe")

# Setting up Selenium
page_to_scrape = webdriver.Chrome(service=browser_driver)
page_to_scrape.get(
    "https://webscraper.io/test-sites/e-commerce/static/computers/laptops")

# Waiting for Accept Cookis popup to load, then clicking accept cookies button:
cookies = WebDriverWait(page_to_scrape, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'acceptCookies')))
cookies.click()

# Setting up our empty list of data
data = []

# Looping through each page, scraping for each product "card", then drilling down to target values
# Then, appending data to our data list for future sorting & writing to CSV
# When the final page is reached, the try/except will trigger a break, and our loop will complete
while True:
    cards = page_to_scrape.find_elements(By.CLASS_NAME, "thumbnail")
    for card in cards:
        name = card.find_element(By.CLASS_NAME, "title").get_attribute("title")
        price = card.find_element(By.CLASS_NAME, "pull-right.price").text
        specs = card.find_element(By.CLASS_NAME, "description").text
        reviews = card.find_element(
            By.CLASS_NAME, "ratings").text.split(" ")[0]
        data.append([name, price, specs, reviews])
    try:
        #You can use XPATH here if unable to find suitable elements to grab by. 
        page_to_scrape.find_element(By.LINK_TEXT, "›").click()
    except NoSuchElementException:
        break

# BONUS: Sorting of data list by PRICE (index 1)
sorted_data = sorted(data, key=lambda row: row[1])

# Looping through data, and writing a new row to our CSV each time
# Using enumerate() to extract index number, and append index + 1 to row
for i, row in enumerate(sorted_data):
    writer.writerow([i + 1] + row)

# Exiting web browser and closing CSV
page_to_scrape.quit()
file.close()
