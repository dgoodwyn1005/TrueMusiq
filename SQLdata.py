import sqlite3

DATABASE_NAME = "song_database.db"

#INFORMATION IN DATABASE
'''
(SONG_NAME, SONG_ARTIST, PLAYLIST, SPOT_IN_PLAYLIST, SONGLINK, SONG_DURATION)
'''

connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

#Create Initial Table
createTable = '''CREATE TABLE IF NOT EXISTS songs(
    song_name TEXT,
    song_artist TEXT,
    playlist TEXT,
    spot_in_playlist INTEGER,
    songlink TEXT,
    duration INT
);
'''

cursor.execute(createTable)

class Database():
    def __init__(self):
        pass

    def display_table(self):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        print("Displaying Table")
        # Execute a query
        cursor.execute("SELECT * FROM songs")
        results = cursor.fetchall()

        # Display the results
        for row in results:
            print(row)

        connection.commit()
        connection.close()

    def add_song(self, data:list):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        name = data[0]
        artist = data[1]
        playlist = data[2]
        spot_in_playlist = data[3]
        songlink = data[4]
        duration = data[5]

        try:
            cursor.execute("INSERT INTO songs(song_name, song_artist, playlist, spot_in_playlist, songlink, duration) VALUES(?, ?, ?, ?, ?, ?)",
                (name, artist, playlist, spot_in_playlist, songlink, duration))
        except sqlite3.Error as e:
            print("Error: %s" % e.args[0])
        
        connection.commit()
        connection.close()

    def find_song(self, column, value):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        results = []
        match column:
            case "name":
                cursor.execute("SELECT song_name FROM songs")
                row = cursor.fetchall()
                for i, info in enumerate(row):
                    if info[0] == value:
                        cursor.execute("SELECT * FROM songs LIMIT 1 OFFSET ?", (str(i)))
                        result = cursor.fetchone()
                        results.append(result)
            case "artist":
                cursor.execute("SELECT song_artist FROM songs")
                row = cursor.fetchall()
                for i, info in enumerate(row):
                    if info[0] == value:
                        cursor.execute("SELECT * FROM songs LIMIT 1 OFFSET ?", (str(i)))
                        result = cursor.fetchone()
                        results.append(result)
            case "playlist":
                cursor.execute("SELECT playlist FROM songs")
                row = cursor.fetchall()
                for i, info in enumerate(row):
                    if info[0] == value:
                        cursor.execute("SELECT * FROM songs LIMIT 1 OFFSET ?", (str(i)))
                        result = cursor.fetchone()
                        results.append(result)

        connection.commit()
        connection.close()

        return results
    
    def add_to_playlist(self, playlist, song_name, song_artist):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        playlist_spot = self.lowest_available_spot(playlist)

        cursor.execute('''UPDATE songs SET playlist = ?, spot_in_playlist = ? WHERE song_name = ? AND song_artist = ?''', (playlist, playlist_spot, song_name, song_artist))

        connection.commit()
        connection.close()

        self.reorder_playlist_spots(playlist)
    
    def lowest_available_spot(self, playlist):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT spot_in_playlist FROM songs WHERE playlist = ?", (playlist,))
            results = cursor.fetchall()
            used_spots = set(row[0] for row in results if row[0] is not None)

            spot = 1
            while spot in used_spots:
                spot += 1
        except sqlite3.Error as e:
            print("Error finding available spot:", e)
            spot = 1

        connection.commit()
        connection.close()

        return spot

    def reorder_playlist_spots(self, playlist):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        try:
            # Get all songs in the playlist, ordered by current spot
            cursor.execute("SELECT rowid, * FROM songs WHERE playlist = ? ORDER BY spot_in_playlist ASC", (playlist,))
            songs = cursor.fetchall()

            # Reassign spots from 1 to len(songs)
            for new_spot, song in enumerate(songs, start=1):
                row_id = song[0]  # Use rowid to uniquely identify the row
                cursor.execute("UPDATE songs SET spot_in_playlist = ? WHERE rowid = ?", (new_spot, row_id))
        except sqlite3.Error as e:
            print("Error reordering playlist spots:", e)

        connection.commit()
        connection.close()
    
    def delete_song(self, data):
        pass

    def get_all_songs(self):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        songs = []
        # Execute a query
        cursor.execute("SELECT * FROM songs")
        results = cursor.fetchall()

        for row in results:
            songs.append(row)

        connection.commit()
        connection.close()

        return songs
    
    def get_all_artists(self):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        artists = []
        # Execute a query
        cursor.execute("SELECT DISTINCT song_artist FROM songs")
        results = cursor.fetchall()

        for row in results:
            artists.append(row)

        connection.commit()
        connection.close()

        return artists

    def get_all_playlists(self):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        # Execute a query
        cursor.execute("SELECT playlist FROM songs")
        playlists = cursor.fetchall()

        true_playlists = []

        for playlist in playlists:
            if playlist[0] != "None" and playlist[0] not in true_playlists:
                true_playlists.append(playlist[0])

        connection.commit()
        connection.close()

        return true_playlists
    
    def get_songs_by_artist(self, artist):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        songs = []
        try:
            cursor.execute("SELECT * FROM songs WHERE song_artist = ?", (artist,))
            songs = cursor.fetchall()
        except sqlite3.Error as e:
            print("Error fetching songs from artist:", e)

        connection.commit()
        connection.close()

        return songs
    
    def get_songs_in_playlist(self, playlist):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        songs = []
        try:
            cursor.execute("SELECT * FROM songs WHERE playlist = ?", (playlist,))
            songs = cursor.fetchall()
        except sqlite3.Error as e:
            print("Error fetching songs from playlist:", e)

        connection.commit()
        connection.close()

        return songs