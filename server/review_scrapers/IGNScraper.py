import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from fuzzywuzzy import fuzz, process
from urllib.parse import urljoin, unquote


# Connect to the SQLite database
conn = sqlite3.connect('../reviewsDB')
cursor = conn.cursor()

def extract_detailed_title_from_url(url):
    """Extract the detailed game title from the review URL."""
    try:
        game_name = url.split('/')[-1].replace('-review', '').replace('-', ' ')
        return unquote(game_name)
    except Exception as e:
        print(f"Error extracting detailed title from URL {url}: {e}")
        return None

def insert_or_fetch_game(conn, title, detailed_title, score_threshold=85):
    cursor = conn.cursor()
    # Use the detailed title for matching if available
    search_title = detailed_title if detailed_title else title
    games = cursor.execute("SELECT GameID, GameName FROM Games").fetchall()
    
    if games:
        closest_match, score = process.extractOne(search_title, [game[1] for game in games], scorer=fuzz.token_sort_ratio)
        if score > score_threshold:
            game_id = [game[0] for game in games if game[1] == closest_match][0]
            print(f"Match found: {closest_match} with score {score}")
            return game_id

    print(f"No match found. Inserting new game: {search_title}")
    cursor.execute("INSERT INTO Games (GameName) VALUES (?)", (search_title,))
    conn.commit()
    return cursor.lastrowid

def insert_review(conn, game_id, original_score, normalized_score, score_scale, source_website, review_url):
    cursor.execute("SELECT * FROM Reviews WHERE GameID = ? AND ReviewURL = ?", (game_id, review_url))
    if cursor.fetchone():
        print(f"Review already exists for GameID {game_id}. Skipping.")
    else:
        cursor.execute("INSERT INTO Reviews (GameID, OriginalScore, NormalizedScore, ScoreScale, SourceWebsite, ReviewURL) VALUES (?, ?, ?, ?, ?, ?)",
                       (game_id, original_score, normalized_score, score_scale, source_website, review_url))
        conn.commit()
        print(f"Inserted review for GameID {game_id}.")

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
base_url = 'https://www.ign.com'

for review in reviews[:40]:
    # Extract the review title using the provided class details
    title_element = review.find('span', class_='interface jsx-1039724788 item-title bold')
    if not title_element:
        continue
    title = title_element.text.strip().replace(' Review', '')

    score_element = review.find('figcaption')
    original_score = score_element.text.strip() if score_element else "N/A"
    normalized_score = original_score 
    score_scale = "10" 

    review_url_element = review.find('a', class_='item-body')
    partial_url = review_url_element['href'] if review_url_element else None
    full_url = urljoin(base_url, partial_url) if partial_url else None
    
    detailed_title = extract_detailed_title_from_url(full_url) if full_url else None

    game_id = insert_or_fetch_game(conn, title, detailed_title, score_threshold=90)
    insert_review(conn, game_id, original_score, normalized_score, score_scale, "IGN", full_url)

    #print(f"Processed review for '{title}' with score '{original_score}' and URL '{full_url}'.")

# Close the browser and database connection
driver.quit()
cursor.close()
conn.close()
