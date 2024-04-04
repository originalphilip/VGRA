import sqlite3

# Connect to database
conn = sqlite3.connect('reviewsDB')
cursor = conn.cursor()

#Create the GameGenres table
cursor.execute('''
CREATE TABLE IF NOT EXISTS GameGenres (
    GameID INTEGER,
    GenreID INTEGER,
    FOREIGN KEY (GameID) REFERENCES Games(GameID),
    FOREIGN KEY (GenreID) REFERENCES Genres(GenreID),
    PRIMARY KEY (GameID, GenreID)
)
''')

# Populate the GameGenres table
cursor.execute('SELECT GameID, Genre FROM Games')
games = cursor.fetchall()

for game_id, genre_string in games:
    if genre_string:  # Check if genre_string is not None
        genres = [genre.strip() for genre in genre_string.split(',')]
        for genre in genres:
            # Get the GenreID for the current genre
            cursor.execute('SELECT GenreID FROM Genres WHERE Name = ?', (genre,))
            genre_id = cursor.fetchone()
            if genre_id:
                # Insert the game-genre association
                cursor.execute('INSERT OR IGNORE INTO GameGenres (GameID, GenreID) VALUES (?, ?)', (game_id, genre_id[0]))

# Commit changes and close the connection
conn.commit()
conn.close()
