from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import urllib.parse
import time
import sqlite3

#connect to database
conn = sqlite3.connect('reviewsDB')

def insert_platforms(conn, platforms):
    platform_ids = []
    cursor = conn.cursor()
    for platform in platforms:
        cursor.execute("SELECT PlatformID FROM Platforms WHERE Name = ?", (platform,))
        result = cursor.fetchone()
        if result:
            platform_ids.append(result[0])
        else:
            cursor.execute("INSERT INTO Platforms (Name) VALUES (?)", (platform,))
            conn.commit()
            platform_ids.append(cursor.lastrowid)
    return platform_ids

def insert_game(conn, game_name, genre, release_date, description, image_url):
    cursor = conn.cursor()
    cursor.execute("SELECT GameID FROM Games WHERE CanonicalName = ?", (game_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO Games (CanonicalName, Genre, ReleaseDate, Description, ImageURL) VALUES (?, ?, ?, ?, ?)",
                       (game_name, genre, release_date, description, image_url))
        conn.commit()
        return cursor.lastrowid
    
def link_game_to_platforms(conn, game_id, platform_ids):
    cursor = conn.cursor()
    for platform_id in platform_ids:
        cursor.execute("INSERT OR IGNORE INTO GamePlatforms (GameID, PlatformID) VALUES (?, ?)", (game_id, platform_id))
    conn.commit()

def insert_review(conn, game_id, original_score, normalized_score, score_scale, source_website, review_url):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Reviews (GameID, OriginalScore, NormalizedScore, ScoreScale, SourceWebsite, ReviewURL) VALUES (?, ?, ?, ?, ?, ?)",
                   (game_id, original_score, normalized_score, score_scale, source_website, review_url))
    conn.commit()

# Setup Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to the URL
driver.get("https://www.metacritic.com/game")

# Wait for dynamic content to load
time.sleep(10)  # Adjust sleep time as needed to ensure the page has fully loaded

# Collect all game review URLs first
games_info = []
links = []
games = driver.find_elements(By.CSS_SELECTOR, "a.c-globalProductCard_container.u-grid")
for game in games:
    # Extract the score text and convert it
    try:
        score_element = game.find_element(By.CSS_SELECTOR, "div[data-v-4cdca868] span[data-v-4cdca868]")
        score_text = score_element.text.strip()
        # Exclude "tbd" scores and convert numeric scores
        if score_text.lower() != "tbd":
            if score_text.isdigit():
                score = float(score_text) / 10  # Adjust score to a scale of 10
            else:
                score = "N/A"
        else:
            continue  # Skip appending this game if score is "tbd"

        # Extract the review link
        review_link = game.get_attribute('href')

        # Extract the image URL
        image_element = game.find_element(By.CSS_SELECTOR, "div.c-globalProductCard_imgContainer img")
        image_url = image_element.get_attribute('src')

        # Add the game's score and review link to the list
        games_info.append((score_text, score, review_link, image_url))
    except Exception as e:
        print(f"Error extracting score: {e}")
        score = "N/A"

# Now navigate to each game's review page to collect additional data
for score_text, score, link, image_url in games_info:
    driver.get(link)
    time.sleep(5)  # Wait for the review page to load

    try:
        # Extract the game title from URL
        title = link.split('/')[-2]
        title = urllib.parse.unquote(title.replace('-', ' '))

        # Extract the release date
        date_element = driver.find_element(By.CSS_SELECTOR, "div.g-text-xsmall span.u-text-uppercase")
        review_date = date_element.text.strip()

        # Extract the game genre
        genre_elements = driver.find_elements(By.CSS_SELECTOR, "div.c-gameDetails_sectionContainer span.c-globalButton_label")
        genres = [genre.text.strip() for genre in genre_elements]

        # Extract the game description
        description_element = driver.find_element(By.CSS_SELECTOR, "span.c-productionDetailsGame_description.g-text-xsmall")
        description = description_element.text.strip()

        # Exttract the compatible platforms
        platform_elements = driver.find_elements(By.CSS_SELECTOR, "div.c-gameDetails_Platforms ul li.c-gameDetails_listItem.g-color-gray70.u-inline-block")
        platforms = [platform.text.strip() for platform in platform_elements]
    except Exception as e:
        print(f"Error extracting data for {link}: {e}")
        title, review_date, genres = "N/A", "N/A", []

    # insert game and review data into corresponding database tables
    platform_ids = insert_platforms(conn, platforms)
    game_id = insert_game(conn, title, " ".join(genres), review_date, description, image_url)
    link_game_to_platforms(conn, game_id, platform_ids)
    insert_review(conn, game_id, score_text, score, 10, 'MetaCritic.com', link)
    #print(f"Title: {title}, Orig Score: {score_text} Score: {score}, Platforms: {platforms} Description: {description}, Review URL: {link}, Image URL: {image_url}, date: {review_date}, genre: {genres}")

conn.close()
# Clean up (close the browser)
driver.quit()
