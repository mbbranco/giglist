# PREPARE DATA
from spotify_api import get_access_token, get_artist_info

# Get access token once (not per artist)
token = get_access_token()

artistas = ['Muse','Charli XCX']
genres = []
bands = []
genres_bands = {}
for b in artistas:
    info = get_artist_info(b, token)
    bands.append((b, info['name'], info['followers'], info['popularity'], info['spotify_url'], info['image_url']))
    genres.append(info['genres'])
    genres_bands[info['name']] = info['genres']


genres_bands_list = []
for k, val in genres_bands.items():
    for v in val:
        genres_bands_list.append((k,v))
    

unique_genres = tuple(set([x for xs in genres for x in xs]))

print(bands)
print(unique_genres)
print(genres_bands_list)

