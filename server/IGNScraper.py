import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
from fuzzywuzzy import process

# Connect to the SQLite database
conn = sqlite3.connect('reviewsDB')
cursor = conn.cursor()

def insert_or_fetch_game(conn, title, source):
    cursor = conn.cursor()
    # Fetch all game titles from the database
    cursor.execute("SELECT GameID, CanonicalName FROM Games")
    games = cursor.fetchall()

    # Use fuzzy matching to find the closest game title
    titles = [game[1] for game in games]  # List of game titles
    closest_match, score = process.extractOne(title, titles)

    # Decide on a threshold for considering a match
    if score > 85:  # Adjust threshold as needed
        game_id = [game[0] for game in games if game[1] == closest_match][0]
        return game_id
    else:
        # If no close match is found, insert the new game
        cursor.execute("INSERT INTO Games (CanonicalName) VALUES (?)", (title,))
        conn.commit()
        return cursor.lastrowid
    
def insert_review(conn, game_id, original_score, normalized_score, score_scale, source_website, review_url):
    if game_id:  # Only insert if game_id is not None (i.e., review does not already exist)
        cursor.execute("INSERT INTO Reviews (GameID, OriginalScore, NormalizedScore, ScoreScale, SourceWebsite, ReviewURL) VALUES (?, ?, ?, ?, ?, ?)",
                       (game_id, original_score, normalized_score, score_scale, source_website, review_url))
        conn.commit()

# Extend scrolling to ensure more reviews are loaded
def scroll_and_load_reviews(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Adjust sleep time as needed for the page to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Setup Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get('https://www.ign.com/reviews/games')
time.sleep(5)

# After setting up the Selenium WebDriver and navigating to the reviews page
scroll_and_load_reviews(driver)  # Call this function to scroll through the page and load more reviews

soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find the common parent elements.
reviews = soup.find_all('div', class_='content-item jsx-1409608325 row divider')
#base_url = 'https://www.ign.com'
review_count = 0  # Counter for reviews processed

for review in reviews:
    if review_count >= 40:
        break  # Stop after processing 40 reviews
    title_element = review.find('span', class_='interface jsx-777404155 item-title bold')
    title = title_element.text.strip().replace('Review', '') if title_element else "Unknown Title"
    
    score_element = review.find('figcaption')
    original_score = score_element.text.strip() if score_element else "N/A"
    
    normalized_score = original_score 
    score_scale = "10"
    
    review_url_element = review.find('a', class_='item-body')
    review_url = review_url_element['href'].strip() if review_url_element and 'href' in review_url_element.attrs else "No URL"

    # Assuming normalized_score calculation and score_scale determination are done previously in your code
    game_id = insert_or_fetch_game(conn, title, "IGN")
    insert_review(conn, game_id, original_score, normalized_score, score_scale, "IGN", review_url)

    
    #print(f"Processed review for {title} from IGN.")
    print(f"Review Title: {title}")
    print(f"Score: {original_score}\n")
    print(f"NS: {normalized_score}\n")
    print(f"Score Scale: {score_scale}\n")
    print(f"URL: {review_url}")
    
    review_count += 1

# Close the browser and database connection
cursor.close()
conn.close()
driver.quit()
