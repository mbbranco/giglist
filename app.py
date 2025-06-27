from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, static_folder='templates/assets')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    selected_sort = request.args.get('sort')
    
    if selected_sort == 'popularity':
        bands = conn.execute('SELECT * FROM bands ORDER BY popularity DESC').fetchall()
    else:
        bands = conn.execute('SELECT * FROM bands ORDER BY name ASC').fetchall()

    selected_genre = request.args.get('genre')
    
    if selected_genre:
        sql = '''
        SELECT * FROM bands
        JOIN genres_bands ON bands.name = genres_bands.band_name
        WHERE genres_bands.genre_name=?
        ORDER BY bands.name DESC
        '''
        bands = conn.execute(sql,(selected_genre,)).fetchall()


    # Get list of distinct venues
    genres_sql = "SELECT DISTINCT genre_name FROM genres_bands ORDER BY genre_name ASC"
    genres = [row['genre_name'] for row in conn.execute(genres_sql).fetchall()]

    conn.close()
    return render_template('index.html', bands=bands,genres=genres)


@app.route('/gigs')
def gigs():
    conn = get_db_connection()

    selected_year = request.args.get('year')
    selected_venue = request.args.get('venue')

    if selected_year and selected_venue:
        sql = '''
        SELECT * FROM gigs 
        JOIN bands ON gigs.band_name = bands.name 
        WHERE strftime('%Y', date) = ?
        AND gigs.venue = ?
        ORDER BY date ASC
        '''
        gigs = conn.execute(sql, (selected_year, selected_venue,)).fetchall()
    elif selected_year and not selected_venue:
        sql = '''
        SELECT * FROM gigs 
        JOIN bands ON gigs.band_name = bands.name 
        WHERE strftime('%Y', date) = ?
        ORDER BY date ASC
        '''
        gigs = conn.execute(sql, (selected_year,)).fetchall()

    elif not selected_year and selected_venue:
        sql = '''
        SELECT * FROM gigs 
        JOIN bands ON gigs.band_name = bands.name 
        WHERE gigs.venue = ?
        ORDER BY date ASC
        '''
        gigs = conn.execute(sql, (selected_venue,)).fetchall()
    else:
        sql = '''
        SELECT * FROM gigs 
        JOIN bands ON gigs.band_name = bands.name 
        ORDER BY date ASC
        '''
        gigs = conn.execute(sql).fetchall()

    # Get list of distinct years
    years_sql = "SELECT DISTINCT strftime('%Y', date) as year FROM gigs ORDER BY year DESC"
    years = [row['year'] for row in conn.execute(years_sql).fetchall()]

    # Get list of distinct venues
    venues_sql = "SELECT DISTINCT venue FROM gigs ORDER BY venue ASC"
    venues = [row['venue'] for row in conn.execute(venues_sql).fetchall()]


    conn.close()
    return render_template('gigs.html', gigs=gigs, years=years, selected_year=selected_year, venues=venues, selected_venue=selected_venue)


if __name__ == '__main__':
    app.run(debug=True)