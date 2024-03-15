from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import urllib.parse
import time

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

    # Print the scraped data
    print(f"Title: {title}, Orig Score: {score_text} Score: {score}, Platforms: {platforms} Description: {description}, Review URL: {link}, Image URL: {image_url}, date: {review_date}, genre: {genres}")

# Clean up (close the browser)
driver.quit()
