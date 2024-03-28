import requests
import sqlite3
from fuzzywuzzy import process
from datetime import datetime, timezone

client_id = 'u8ztv2mgn5yvntus43u1rnpiyhksu0'
client_secret = 'vuvc91kbyfpf4g72vvjum9alszr933'

# Getting the access token
url = 'https://id.twitch.tv/oauth2/token'
params = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials'
}
response = requests.post(url, params=params)
response_json = response.json()

access_token = response_json['access_token']
headers = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

# Connect to reviews database
conn = sqlite3.connect('ReviewsDB')
cursor = conn.cursor()

def insert_or_fetch_game(name, genre_names, release_date, description, image_url):
    cursor.execute("SELECT GameID, CanonicalName, ReleaseDate FROM Games")
    games = cursor.fetchall()
    # Adjusted fuzzy matching logic with release date consideration
    closest_match, similarity = None, 0
    for game in games:
        current_similarity = process.extractOne(name, [game[1]])[1]
        # Additional check for release year to improve matching accuracy
        game_release_year = datetime.strptime(game[2], '%Y-%m-%d').year if game[2] else None
        query_release_year = datetime.strptime(release_date, '%Y-%m-%d').year if release_date else None
        if current_similarity > similarity and game_release_year == query_release_year:
            closest_match, similarity = game, current_similarity

    if similarity > 85:  # Adjusted threshold
        game_id = closest_match[0]
        # Verify if update is necessary before executing
        cursor.execute("SELECT Genre, ReleaseDate, Description, ImageURL FROM Games WHERE GameID = ?", (game_id,))
        existing_info = cursor.fetchone()
        if (genre_names, release_date, description, image_url) != existing_info:
            cursor.execute("UPDATE Games SET Genre = ?, ReleaseDate = ?, Description = ?, ImageURL = ? WHERE GameID = ?",
                           (genre_names, release_date, description, image_url, game_id))
            conn.commit()
    else:
        # Insert a new game entry with a verification step if needed
        cursor.execute("INSERT INTO Games (CanonicalName, Genre, ReleaseDate, Description, ImageURL) VALUES (?, ?, ?, ?, ?)",
                       (name, genre_names, release_date, description, image_url))
        conn.commit()
        game_id = cursor.lastrowid

    return game_id


def search_igdb_for_title(title):
    '''Search IGDB for a title and return a list of potential matches'''
    data = f'search "{title}"; fields name, genres.name, platforms.name, first_release_date, summary, cover.url;'
    response = requests.post(url, headers=headers, data=data)
    return response.json()

def get_best_match(search_title, search_results):
    '''Find the best match for a title from a list of search results'''
    titles = [result['name'] for result in search_results]
    if titles:
        best_match, score = process.extractOne(search_title, titles)
        if score >= 90:
            return next((result for result in search_results if result['name'] == best_match), None)
    return None


# Function to insert or fetch a platform and return its ID
def insert_or_fetch_platform(platform_name):
    cursor.execute("SELECT PlatformID FROM Platforms WHERE Name = ?", (platform_name,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO Platforms (Name) VALUES (?)", (platform_name,))
        conn.commit()
        return cursor.lastrowid
    return result[0]

# Query database for the list of game titles reviewed
cursor.execute("SELECT DISTINCT CanonicalName FROM Games")
games = cursor.fetchall()

# Define the base URL for the IGDB API games endpoint
url = 'https://api.igdb.com/v4/games'

for game_title_tuple in games:
    game_title = game_title_tuple[0]
    search_results = search_igdb_for_title(game_title)
    
    best_match = get_best_match(game_title, search_results)
    if best_match:
        # Use best_match directly since it contains the game information
        name = best_match.get('name', 'No Name Available')
        platforms = [platform['name'] for platform in best_match.get('platforms', [])]  # Fetch platforms
        genre_names = ', '.join([genre['name'] for genre in best_match.get('genres', [])])
        release_date = datetime.fromtimestamp(best_match.get('first_release_date', 0), tz=timezone.utc).strftime('%Y-%m-%d') if best_match.get('first_release_date') else 'No Release Date Available'
        description = best_match.get('summary', 'No Description Available')
        image_url = f"https:{best_match.get('cover', {}).get('url', '').replace('t_thumb', 't_cover_big')}" if best_match.get('cover') else 'No Image Available'

        game_id = insert_or_fetch_game(name, genre_names, release_date, description, image_url)
        print(f"Name: {name}")
        print(f"Genres: {genre_names}")
        print(f"Release Date: {release_date}")
        print(f"Description: {description}")
        print(f"Image URL: {image_url}")
        print("="*100)

        for platform_name in platforms:
            platform_id = insert_or_fetch_platform(platform_name)
            cursor.execute("SELECT * FROM GamePlatforms WHERE GameID = ? AND PlatformID = ?", (game_id, platform_id))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO GamePlatforms (GameID, PlatformID) VALUES (?, ?)", (game_id, platform_id))
                conn.commit()
    else:
        print(f"No accurate match found for {game_title}")

    cursor.execute("""
    UPDATE Games SET
    Genre = ?,
    ReleaseDate = ?,
    Description = ?,
    ImageURL = ?
    WHERE CanonicalName = ?
    """, (genre_names, release_date, description, image_url, name))

conn.close()