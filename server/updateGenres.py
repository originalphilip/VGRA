import sqlite3

conn = sqlite3.connect('reviewsDB')
cursor = conn.cursor()

cursor.execute('SELECT Genre FROM Games')
rows = cursor.fetchall()

genres = set()
for row in rows:
    if row[0]:
        genres.update([genre.strip() for genre in row[0].split(',')])

for genre in genres:
    cursor.execute('INSERT OR IGNORE INTO Genres (Name) VALUES (?)', (genre,))

conn.commit()
conn.close()
