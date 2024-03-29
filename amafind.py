import csv
from http import server
from bs4 import BeautifulSoup
from numpy import true_divide
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import os
import getpass

# User input variables
csv_file_name = input(str("What would you like to name your CSV file? "))
item_search = input(str("What item would you like to search for? "))
print(f"Now searching results for {item_search}...")

# Create URL for search item
def get_url(search_term):
    template = 'https://www.amazon.ca/s?k={}s&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')

    # add the term query to URL
    url = template.format(search_term)
    url += '&page={}'
    
    # rate limiting
    time.sleep(1)
    
    return url

# Extract content from page
def extract_record(item):
    # Extract/return data from a single record

    # Description
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.ca/' + atag.get('href')

    # Debug and negative testing
    try:
        # Price 
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return 

    try:
        # Ratings/count
        rating = item.find('span', {'class': 'a-icon-alt'}).text
        review_count = item.find('span', {'class': 'a-size-base'}).text
    except AttributeError:
        rating = '0'
        review_count = '0'

    result = (description, price, rating, review_count, url)
    return result


def main(search_term):
    user = getpass.getuser()
    # Replace with path of where chromedriver is located
    s = Service(f'/Users/{user}/Documents/Develop/amazon_web_scraper/amafind/chromedriver')
    driver = webdriver.Chrome(service=s)

    records = []
    url = get_url(search_term)

    # Amazon displays 20 pages -> run 20 times
    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    print(f"Search results for {item_search} are now completed!")
    driver.close()

    # Save data to CSV file
    csv_file_path = '/Users/ericxie/Documents/Develop/amazon_web_scraper/CSV_files/'

    path = os.path.join(csv_file_path, csv_file_name + '.csv')

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'Review Count', 'URL'])
        writer.writerows(records)

# Execute code
main(item_search)