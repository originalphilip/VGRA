import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import urllib.parse
import time
import sqlite3

conn = sqlite3.connect('../reviewsDB')

def insert_game(conn, game_name):
    cursor = conn.cursor()
    cursor.execute("SELECT GameID FROM Games WHERE GameName = ?", (game_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO Games (GameName) VALUES (?)", (game_name,))
        conn.commit()
        return cursor.lastrowid
    
def insert_review(conn, game_id, original_score, normalized_score, score_scale, source_website, review_url):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Reviews (GameID, OriginalScore, NormalizedScore, ScoreScale, SourceWebsite, ReviewURL) VALUES (?, ?, ?, ?, ?, ?)",
                   (game_id, original_score, normalized_score, score_scale, source_website, review_url))
    conn.commit()

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.metacritic.com/game")

time.sleep(10)

# collect all game review URL first
games_info = []
links = driver.find_elements(By.CSS_SELECTOR, "a.c-globalProductCard_container.u-grid")
for link in links:
    games_info.append(link.get_attribute('href'))

# navigate to each games review page to collect additional data
for link in games_info:
    driver.get(link)
    time.sleep(5)

    try:
        # extract the game title from URL
        title_element = driver.find_element(By.CSS_SELECTOR, ".c-productHero_title > div")
        title = title_element.text.strip()
        
        # extract the score text and convert it
        score_element = driver.find_element(By.CSS_SELECTOR, "div[data-v-4cdca868] span[data-v-4cdca868]")
        original_score_text = score_element.text.strip()

        # check if the score is 'tbd', and if so, skip to the next game
        if original_score_text .lower() == 'tbd':
            print(f"Skipping {title} as the score is TBD.")
            continue  # skip the rest of the loop and move to the next game

        print(f"Processing game: {title} with score: {original_score_text}")
        
        # metacritic scores are out of 100, convert this to a scale of 10 for normalized score
        normalized_score = round(float(original_score_text) / 10, 1) if original_score_text.isdigit() else None

        # extract the review link
        review_link = link

    except Exception as e:
        print(f"Error extracting data for {link}: {e}")
        continue

    game_id = insert_game(conn, title)
    score_scale = "100"  # Metacritic's score scale is out of 100
    insert_review(conn, game_id, original_score_text, normalized_score, score_scale, 'MetaCritic.com', review_link)

conn.close()
driver.quit()
