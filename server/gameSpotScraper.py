import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# def insert_review(conn, game_name, score, review_url):
#     cursor = conn.cursor()
#     # Insert game review logic here
#     print(f"Inserting: {game_name}, Score: {score}, URL: {review_url}")
#     # insertion code
#     cursor.execute("INSERT INTO Reviews (game_name, score, review_url) VALUES (?, ?, ?)", (game_name, score, review_url))
#     conn.commit()

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
    conn = sqlite3.connect('ReviewsDB copy')

    # Find all review elements
    reviews = driver.find_elements(By.CSS_SELECTOR, ".card-item__main")

    for review in reviews:
        try:
            # Extract the game title and review URL
            link_element = review.find_element(By.CSS_SELECTOR, "a.card-item__link")
            review_url = link_element.get_attribute('href')
            game_name = link_element.find_element(By.CSS_SELECTOR, "h4.card-item__title").text.replace(" Review", "")
        
            # Correct the URL if it doesn't start with 'http'
            if not review_url.startswith('http'):
                review_url = f"https://www.gamespot.com{review_url}"

            # Extract the score
            score_element = review.find_element(By.CSS_SELECTOR, ".review-ring-score__score")
            score = score_element.text.strip()

            # Insert review data into the database
            # insert_review(conn, game_name, score, review_url)
            print(f"Game Name: {game_name}, Score: {score}, URL: {review_url}")
            
        except Exception as e:
            print(f"Error scraping review: {e}")
            continue

    # Close the browser and database connection
    driver.quit()
    conn.close()

if __name__ == "__main__":
    scrape_gamespot_reviews()
