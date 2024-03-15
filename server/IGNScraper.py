import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import traceback
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('reviewDB')
cursor = conn.cursor()

    
# Setup Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to the URL
driver.get('https://www.ign.com/reviews/games')

# Wait for dynamic content to load
driver.implicitly_wait(10)  # Waits up to 10 seconds for elements to become available

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for new content to load
    time.sleep(5)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        
        break
    last_height = new_height


soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find the common parent elements.
common_parents = soup.find_all('div', class_='content-item jsx-1409608325 row divider')

base_url = 'https://www.ign.com'

# A function to parse the relative date string and return the actual date
def parse_relative_date(date_str):
    today = datetime.today()

    # Check for relative date formats first
    if 'd ago' in date_str:
        num = int(date_str.split('d ago')[0])
        return today - timedelta(days=num)
    elif 'h ago' in date_str:
        num = int(date_str.split('h ago')[0])
        return today - timedelta(hours=num)
    elif 'm ago' in date_str:
        num = int(date_str.split('m ago')[0])
        return today - timedelta(minutes=num)
    elif 'w ago' in date_str:
        num = int(date_str.split('w ago')[0])
        return today - timedelta(weeks=num)
    else:
        # Handle absolute dates
        try:
            # Attempt to parse the date using the known format
            return datetime.strptime(date_str, '%b %d, %Y')
        except ValueError:
            # If parsing fails, print an error and return today's date as a fallback
            print(f"Unrecognized date format: {date_str}")
            return today


print(parse_relative_date("5d ago"))  # Relative date
print(parse_relative_date("Jul 5, 2023"))  # Absolute date



for parent in common_parents:
    # Within each parent, find the title and the score
    title_element = parent.find('span', class_='interface jsx-777404155 item-title bold')
    if title_element:
        title = title_element.text.strip()
        # Remove the word "Review" from the title if present
        title = title.replace('Review', '') 
    else:
        title = "Unknown Title"
    score = parent.find('figcaption').text.strip()  # Assuming score is directly within figcaption
    a_tag = parent.find('a', class_='item-body')  # Correctly target the <a> tag with class "item-body"
    date_element = parent.find('div', class_='interface jsx-153568585 jsx-957202555 item-subtitle small')
    
    if date_element:
        date_text = date_element.text.split('-')[0].strip()  # Assuming the format is "5d ago - Description"
        review_date = parse_relative_date(date_text)
        # Format the review_date as a string if necessary
        review_date_str = review_date.strftime('%Y-%m-%d')
    else:
        review_date_str = 'Unknown'

    
    if a_tag and 'href' in a_tag.attrs:
        review_url = a_tag['href'].strip()  # Get the href attribute
        
        # Check if the URL is relative and prepend the base URL if necessary
        if not review_url.startswith('http'):
            review_url = base_url + review_url
        
        source = "IGN"
        
        # Insert the data into the database
        # cursor.execute("INSERT INTO game_reviews (game_title, review_score, review_date, source, review_url) VALUES (?, ?, ?, ?, ?)",
        #                (title, score, review_date_str, source, review_url))
                       
        # # Commit the transaction
        # conn.commit()
        
        print(f"Review Title: {title}")
        print(f"Review Date: {review_date_str}")
        print(f"Score: {score}\n")
        print(f"Source: {source}\n")
        print(f"URL: {review_url}\n")
    else:
        print("No review URL found within the specified <a> tag.")
        
# Close the cursor and the database connection
cursor.close()
conn.close()

# Don't forget to close the driver
driver.quit()
