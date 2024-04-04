import sqlite3

# Connect to your database
conn = sqlite3.connect('reviewsDB')
cursor = conn.cursor()

# Fetch all genres
cursor.execute('SELECT Genre FROM Games')
rows = cursor.fetchall()

# Split and deduplicate genres
genres = set()
for row in rows:
    if row[0]:  # Check if genre is not None
        genres.update([genre.strip() for genre in row[0].split(',')])

# Insert unique genres
for genre in genres:
    cursor.execute('INSERT OR IGNORE INTO Genres (Name) VALUES (?)', (genre,))

# Commit and close
conn.commit()
conn.close()
