import requests
import sqlite3
from fuzzywuzzy import process, fuzz
from datetime import datetime, timezone

client_id = 'u8ztv2mgn5yvntus43u1rnpiyhksu0'
client_secret = 'vuvc91kbyfpf4g72vvjum9alszr933'

# Getting the access token
auth_url = 'https://id.twitch.tv/oauth2/token'  # Use 'auth_url' for clarity
params = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials'
}
response = requests.post(auth_url, params=params)
response_json = response.json()

access_token = response_json['access_token']
headers = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

# Connect to reviews database
conn = sqlite3.connect('ReviewsDB Copy')
cursor = conn.cursor()

def find_closest_game(name, candidates):
    """Find the closest match for a game name from a list of candidates."""
    best_match, best_score = process.extractOne(name, candidates, scorer=fuzz.token_set_ratio)
    return best_match if best_score > 85 else None

def update_game_if_exists(name, release_date, description, image_url):
    cursor.execute("SELECT GameID, CanonicalName FROM Games")
    games = cursor.fetchall()
    game_names = [game[1] for game in games]
    
    closest_match = find_closest_game(name, game_names)
    
    if closest_match:
        game_id = [game[0] for game in games if game[1] == closest_match][0]
        print(f"Found a close match for '{name}': '{closest_match}'. Updating details.")
        cursor.execute("""
            UPDATE Games 
            SET ReleaseDate = ?, Description = ?, ImageURL = ?
            WHERE GameID = ?""",
            (release_date, description, image_url, game_id))
        conn.commit()
        return game_id
    else:
        print(f"No close match found for '{name}'. No action taken.")
        return None

def search_igdb_for_title(title):
    igdb_url = 'https://api.igdb.com/v4/games'  # Ensure this is the correct endpoint
    data = f'search "{title}"; fields name, genres.name, platforms.name, first_release_date, summary, cover.url;'
    response = requests.post(igdb_url, headers=headers, data=data)
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

def insert_or_fetch_genre(genre_name):
    cursor.execute("SELECT GenreID FROM Genres WHERE Name = ?", (genre_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO Genres (Name) VALUES (?)", (genre_name,))
        conn.commit()
        return cursor.lastrowid


def handle_special_cases(title):
    # Define known special cases and how to handle them
    special_cases = {
        "early access": lambda t: t.replace("early access", "").strip(),
        "dlc": lambda t: t  # Might decide not to alter "DLC" titles, or implement a specific strategy
    }
    
    # Check and handle each special case
    for case, handler in special_cases.items():
        if case.lower() in title.lower():
            print(f"Handling special case for '{title}': '{case}'")
            title = handler(title)
    
    return title

# Query database for the list of game titles reviewed
cursor.execute("SELECT DISTINCT CanonicalName FROM Games")
games = cursor.fetchall()

# Define the base URL for the IGDB API games endpoint
url = 'https://api.igdb.com/v4/games'

for game_title_tuple in games:
    game_title = game_title_tuple[0]
    game_title_modified = handle_special_cases(game_title)
    search_results = search_igdb_for_title(game_title_modified)
    
    best_match = get_best_match(game_title_modified, search_results)
    if best_match:
        # Use best_match directly since it contains the game information
        name = best_match.get('name', 'No Name Available')
        platforms = [platform['name'] for platform in best_match.get('platforms', [])]  # Fetch platforms
        genre_names = ', '.join([genre['name'] for genre in best_match.get('genres', [])])
        release_date = datetime.fromtimestamp(best_match.get('first_release_date', 0), tz=timezone.utc).strftime('%Y-%m-%d') if best_match.get('first_release_date') else 'No Release Date Available'
        description = best_match.get('summary', 'No Description Available')
        image_url = f"https:{best_match.get('cover', {}).get('url', '').replace('t_thumb', 't_cover_big')}" if best_match.get('cover') else 'No Image Available'

        game_id = update_game_if_exists(name, release_date, description, image_url)
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
        
        genre_ids = [insert_or_fetch_genre(genre_name) for genre_name in genre_names.split(', ')]
        for genre_id in genre_ids:
            cursor.execute("INSERT OR IGNORE INTO GameGenres (GameID, GenreID) VALUES (?, ?)", (game_id, genre_id))
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