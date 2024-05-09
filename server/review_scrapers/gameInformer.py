import sqlite3
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fuzzywuzzy import fuzz, process
from selenium.common.exceptions import TimeoutException, NoSuchElementException,ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def normalize_game_name(game_name):
    normalized_name = re.sub(r' - .*', '', game_name).strip()
    normalized_name = normalized_name.replace(' - ', ': ')
    return normalized_name.lower()

def insert_or_fetch_game(conn, game_name, detailed_game_name, score_threshold=75):
    normalized_name = normalize_game_name(game_name)
    cursor = conn.cursor()
    cursor.execute("SELECT GameID, GameName FROM Games")
    games = cursor.fetchall()
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

def scrape_gameinformer_reviews():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.gameinformer.com/reviews")
    wait = WebDriverWait(driver, 20)
    
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ds-main .views-row")))
        conn = sqlite3.connect('../ReviewsDB')

        # attempt to close any potential overlays first
        try:
            # example: close cookie consent or any overlay, update the selector as needed
            close_button = driver.find_element(By.CSS_SELECTOR, "button.cookie-consent-close")
            close_button.click()
        except NoSuchElementException:
            print("No overlay button found.")

        # handling dynamic content loading
        while True:
            try:
                load_more_button = driver.find_element(By.CSS_SELECTOR, 'a.button[rel="next"]')
                # use JavaScript to perform the click to bypass overlay issues
                driver.execute_script("arguments[0].click();", load_more_button)
                # wait to ensure the page has loaded new content
                WebDriverWait(driver, 10).until(EC.staleness_of(load_more_button))
            except NoSuchElementException:
                print("No more 'Load More' button found.")
                break
            except TimeoutException:
                print("Timeout while waiting for new content to load.")
                break

        reviews = driver.find_elements(By.CSS_SELECTOR, "div.views-row")
        for review in reviews:
            try:
                link_element = review.find_element(By.CSS_SELECTOR, "h2.page-title a")
                review_url = link_element.get_attribute('href')
                game_title = review.find_element(By.CSS_SELECTOR, "div.field__items").text.strip()
                score = review.find_element(By.CSS_SELECTOR, "div.score div.field__item").text.strip()
                normalized_score = score
                score_scale = "10"
                
                game_id = insert_or_fetch_game(conn, game_title, game_title)
                insert_review(conn, game_id, score, normalized_score, score_scale, "GameInformer", review_url)
                
                print(f"Inserted game: {game_title}, Score: {score}, URL: {review_url}")
                
            except Exception as e:
                print(f"Error scraping review: {e}")
                continue
        driver.quit()
        conn.close()
    except TimeoutException:
        print("Failed to load all reviews within the allotted time.")
        driver.quit()
        return  # exit if elements are not loaded

if __name__ == "__main__":
    scrape_gameinformer_reviews()