# create_db.py
import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Drop existing tables (if they exist)
cur.execute('DROP TABLE IF EXISTS bands')
cur.execute('DROP TABLE IF EXISTS gigs')


# Create tables
cur.execute('''
CREATE TABLE bands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    spotify_name TEXT,
    followers INT,
    popularity INT,   
    spotify_url TEXT,
    image_url TEXT        
)
''')

cur.execute('''
CREATE TABLE gigs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    band_name TEXT,
    date DATE,
    venue TEXT
)
''')


# Get Data from Sheets
import pandas as pd 

# Google Sheets shareable link
sheet_url = "https://docs.google.com/spreadsheets/d/13E3riRnZSP8SI-10lcAhMSlFX_c9J-PcrGTyCrCSVyU/edit?usp=sharing"

# Convert to CSV export URL
csv_url = sheet_url.replace('/edit?usp=sharing', '/export?format=csv')

# Read the sheet into a DataFrame
df = pd.read_csv(csv_url)


# PREPARE DATA
from spotify_api import get_access_token, get_artist_info

# Get access token once (not per artist)
token = get_access_token()

bands = []
for b in df['Artista'].unique():
    info = get_artist_info(b, token)
    bands.append((b, info['name'], info['followers'], info['popularity'], info['spotify_url'], info['image_url']))
    if b!=info['name']:
        print(b)

gigs = []
for i,g in df.iterrows():
    gigs.append((g['Artista'],g['Data'],g['Local']))
   
# POPULATE DATA
cur.executemany('INSERT INTO bands (name,spotify_name,followers,popularity,spotify_url,image_url) VALUES (?,?,?,?,?,?)', bands)
cur.executemany('INSERT INTO gigs (band_name, date, venue) VALUES (?, ?, ?)', gigs)

conn.commit()
conn.close()