import sqlite3
# This is script to remove duplicate platforms and update the corresponding games platformID

def query_database(query):
    """Executes a SQL query and returns the result."""
    conn = sqlite3.connect('ReviewsDB')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def execute_database(command):
    """Executes a SQL command without returning any results."""
    conn = sqlite3.connect('ReviewsDB')
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()
    conn.close()

duplicates_mapping = {
    'PC (Microsoft Windows)': 'PC',
    'Xbox Series X': 'Xbox Series X|S',
    # add other duplicates as needed
}

for duplicate, primary in duplicates_mapping.items():
    # find the PlatformIDs based on the name
    primary_id = query_database(f"SELECT PlatformID FROM Platforms WHERE Name = '{primary}'")
    duplicate_id = query_database(f"SELECT PlatformID FROM Platforms WHERE Name = '{duplicate}'")
    
    if primary_id and duplicate_id:
        # reassign games from the duplicate to the primary platform
        execute_database(f"UPDATE GamePlatforms SET PlatformID = {primary_id} WHERE PlatformID = {duplicate_id}")
    
        # delete the duplicate platform
        execute_database(f"DELETE FROM Platforms WHERE PlatformID = {duplicate_id}")
        print(f"Merged and removed {duplicate} into {primary}")
    else:
        print(f"Could not find IDs for '{primary}' or '{duplicate}'.")
