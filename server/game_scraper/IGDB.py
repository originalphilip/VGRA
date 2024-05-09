import requests
import sqlite3
from fuzzywuzzy import process, fuzz
from datetime import datetime, timezone

client_id = 'u8ztv2mgn5yvntus43u1rnpiyhksu0'
client_secret = 'vuvc91kbyfpf4g72vvjum9alszr933'

# Getting the access token
auth_url = 'https://id.twitch.tv/oauth2/token'
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
conn = sqlite3.connect('../ReviewsDB')
cursor = conn.cursor()

def find_closest_game(name, candidates):
    """Find the closest match for a game name from a list of candidates."""
    best_match, best_score = process.extractOne(name, candidates, scorer=fuzz.token_set_ratio)
    return best_match if best_score > 85 else None

def update_game_if_exists(name, release_date, description, image_url):
    cursor.execute("SELECT GameID, GameName FROM Games")
    games = cursor.fetchall()
    closest_match = process.extractOne(name, [game[1] for game in games], scorer=fuzz.token_set_ratio)[0]
    if closest_match:
        game_id = next(game[0] for game in games if game[1] == closest_match)
        cursor.execute("UPDATE Games SET ReleaseDate = ?, Description = ?, ImageURL = ? WHERE GameID = ?",
                       (release_date, description, image_url, game_id))
        conn.commit()
        return game_id
    return None

def search_igdb(title, category_filter=None):
    url = 'https://api.igdb.com/v4/games'
    data = f'search "{title}"; fields name, platforms.name, genres.name, first_release_date, summary, cover.url;'
    if category_filter:
        data += f' where category = ({category_filter});'
    response = requests.post(url, headers=headers, data=data)
    return response.json()

def handle_title(title):
    # Add logic to modify the title or decide on category based on specific keywords
    category_filter = '1,2' if 'dlc' in title.lower() or 'expansion' in title.lower() else None
    return title.replace('dlc', '').replace('expansion', '').strip(), category_filter

def get_best_match(search_title, search_results):
    titles = [result['name'] for result in search_results]
    if titles:
        best_match, score = process.extractOne(search_title, titles)
        if score >= 90:
            return next((result for result in search_results if result['name'] == best_match), None)
    return None

def handle_special_cases(title):
    modified_title = title.replace('DLC', '').strip()
    return modified_title, 'DLC' in title or 'Expansion' in title

# Function to insert or fetch a platform and return its ID
def insert_or_update_platforms(game_id, platform_names):
    for platform_name in platform_names:
        cursor.execute("SELECT PlatformID FROM Platforms WHERE Name = ?", (platform_name,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO Platforms (Name) VALUES (?)", (platform_name,))
            conn.commit()
            platform_id = cursor.lastrowid
        else:
            platform_id = result[0]

        cursor.execute("INSERT OR IGNORE INTO GamePlatforms (GameID, PlatformID) VALUES (?, ?)", (game_id, platform_id))
    conn.commit()

def insert_or_fetch_genre(genre_name):
    cursor.execute("SELECT GenreID FROM Genres WHERE Name = ?", (genre_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO Genres (Name) VALUES (?)", (genre_name,))
        conn.commit()
        return cursor.lastrowid

cursor.execute("SELECT DISTINCT GameName FROM Games")
games = cursor.fetchall()

for game in games:
    title, category_filter = handle_title(game[0])
    results = search_igdb(title, category_filter)
    best_match = next((res for res in results if fuzz.token_set_ratio(res['name'], title) > 85), None)
    
    if best_match:
        # Extract details and update database
        name = best_match['name']
        platforms = [plat['name'] for plat in best_match.get('platforms', [])] 
        genres = [gen['name'] for gen in best_match.get('genres', [])]
        release_date = datetime.utcfromtimestamp(best_match['first_release_date']).strftime('%Y-%m-%d') if 'first_release_date' in best_match else 'Unknown'
        description = best_match.get('summary', 'No description provided.')
        image_url = f"https:{best_match['cover']['url'].replace('t_thumb', 't_cover_big')}" if 'cover' in best_match else 'No image available.'
        
        game_id = update_game_if_exists(name, release_date, description, image_url)
        print(f"Updated {name} in the database with ID {game_id}.")
        
        insert_or_update_platforms(game_id, platforms)  # Ensure platforms is a list

        # for platform_name in platforms:
        #     platform_id = insert_or_update_platforms(game_id, platform_name)
        #     cursor.execute("INSERT OR IGNORE INTO GamePlatforms (GameID, PlatformID) VALUES (?, ?)", (game_id, platform_id))
        #     conn.commit()

        for genre_name in genres:
            genre_id = insert_or_fetch_genre(genre_name)
            cursor.execute("INSERT OR IGNORE INTO GameGenres (GameID, GenreID) VALUES (?, ?)", (game_id, genre_id))
        conn.commit()

    else:
        print(f"No accurate match found for {title}")

conn.close()