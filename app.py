from flask import Flask, render_template
import sqlite3

app = Flask(__name__, static_folder='templates/assets')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    bands = conn.execute('SELECT * FROM bands ORDER BY popularity DESC').fetchall()
    conn.close()
    return render_template('index.html', bands=bands)

@app.route('/gigs')
def gigs():
    conn = get_db_connection()
    sql = 'SELECT * FROM gigs ' \
    'INNER JOIN bands ON gigs.band_name = bands.name '\
    'ORDER BY date ASC '
    gigs = conn.execute(sql).fetchall()
    conn.close()
    return render_template('gigs.html', gigs=gigs)

if __name__ == '__main__':
    app.run(debug=True)