import sqlite3

conn = sqlite3.connect('reviewsDB')
cursor = conn.cursor()

#create the GameGenres table
cursor.execute('''
CREATE TABLE IF NOT EXISTS GameGenres (
    GameID INTEGER,
    GenreID INTEGER,
    FOREIGN KEY (GameID) REFERENCES Games(GameID),
    FOREIGN KEY (GenreID) REFERENCES Genres(GenreID),
    PRIMARY KEY (GameID, GenreID)
)
''')

cursor.execute('SELECT GameID, Genre FROM Games')
games = cursor.fetchall()

for game_id, genre_string in games:
    if genre_string: 
        genres = [genre.strip() for genre in genre_string.split(',')]
        for genre in genres:
            cursor.execute('SELECT GenreID FROM Genres WHERE Name = ?', (genre,))
            genre_id = cursor.fetchone()
            if genre_id:
                cursor.execute('INSERT OR IGNORE INTO GameGenres (GameID, GenreID) VALUES (?, ?)', (game_id, genre_id[0]))

conn.commit()
conn.close()
