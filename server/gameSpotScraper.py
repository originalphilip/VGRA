import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fuzzywuzzy import fuzz, process
import re

def normalize_game_name(game_name):
    # Remove any subgame_names or descriptions after a hyphen or dash and trim spaces
    normalized_name = re.sub(r' - .*', '', game_name).strip()
    # Replace various forms of punctuation to maintain consistency
    normalized_name = normalized_name.replace(' - ', ': ')
    return normalized_name.lower()  # Convert to lowercase for case-insensitive comparison

def insert_or_fetch_game(conn, game_name, detailed_game_name, score_threshold=75):
    normalized_name = normalize_game_name(game_name)
    cursor = conn.cursor()
    cursor.execute("SELECT GameID, GameName FROM Games")
    games = cursor.fetchall()
    
    # Use a better-suited scoring method for this use case
    if games:
        closest_match, score = process.extractOne(normalized_name, [game[1].lower() for game in games], scorer=fuzz.partial_ratio)
        if score > score_threshold:
            game_id = [game[0] for game in games if game[1].lower() == closest_match][0]
            print(f"Match found: {closest_match} with score {score}")
            return game_id

    print(f"No match found. Inserting new game: {normalized_name}")
    cursor.execute("INSERT INTO Games (GameName) VALUES (?)", (normalized_name,))
    conn.commit()
    return cursor.lastrowid

def insert_review(conn, game_id, original_score, normalized_score, score_scale, source_website, review_url):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Reviews (GameID, OriginalScore, NormalizedScore, ScoreScale, SourceWebsite, ReviewURL) VALUES (?, ?, ?, ?, ?, ?)",
                   (game_id, original_score, normalized_score, score_scale, source_website, review_url))
    conn.commit()

def scrape_gamespot_reviews():
    # Initialize Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.gamespot.com/games/reviews/")
    

    # Initialize WebDriverWait with a timeout of 10 seconds
    wait = WebDriverWait(driver, 10)

    # Wait for the review elements to be loaded and visible
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".card-item__main")))


    # Connect to the SQLite database
    conn = sqlite3.connect('ReviewsDB')

    # Find all review elements
    reviews = driver.find_elements(By.CSS_SELECTOR, ".card-item__main")

    for review in reviews:
        try:
            # Extract the game game_name and review URL
            link_element = review.find_element(By.CSS_SELECTOR, "a.card-item__link")
            review_url = link_element.get_attribute('href')
            detailed_game_name = link_element.find_element(By.CSS_SELECTOR, "h4.card-item__title").text.replace(" Review", "")
            game_name = detailed_game_name

            # Correct the URL if it doesn't start with 'http'
            if not review_url.startswith('http'):
                review_url = f"https://www.gamespot.com{review_url}"
                
            # Extract the score
            score_element = review.find_element(By.CSS_SELECTOR, ".review-ring-score__score")
            score = score_element.text.strip()
            normalized_score = score
            score_scale = "10"
            

            # Insert game and review data into the database
            game_id = insert_or_fetch_game(conn, game_name, detailed_game_name)
            insert_review(conn, game_id, score, normalized_score, score_scale, "GameSpot", review_url)
            
            print(f"Inserted game: {detailed_game_name}, Score: {score}, URL: {review_url}")
            
        except Exception as e:
            print(f"Error scraping review: {e}")
            continue

    # Close the browser and database connection
    driver.quit()
    conn.close()

if __name__ == "__main__":
    scrape_gamespot_reviews()
