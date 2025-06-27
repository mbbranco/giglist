import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db_connection()
sql = 'SELECT * FROM gigs ' \
'INNER JOIN bands ON gigs.band_name = bands.name '\
'ORDER BY date ASC '
gigs = conn.execute(sql).fetchall()

print(gigs)