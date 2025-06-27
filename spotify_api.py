# get data about bands from Spotify API
import pandas as pd
import requests

# Replace these with your Spotify app credentials
CLIENT_ID = '12f328b526c44308ad85508dbbac698a'
CLIENT_SECRET = '779b7cc6bc024403ae2ae7d142f3edbc'

def get_access_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    return auth_response.json().get('access_token')

def get_artist_info(artist_name,token):
    if not artist_name:
        raise ValueError('Artist name is required')
    
    headers = {'Authorization': f'Bearer {token}'}
    search_url = 'https://api.spotify.com/v1/search'
    params = {'q': artist_name, 'type': 'artist', 'limit': 1}
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()

    if not data.get('artists', {}).get('items'):
        return None

    artist = data['artists']['items'][0]
    artist_info = {
        'name': artist['name'],
        'genres': artist['genres'],
        'followers': artist['followers']['total'],
        'popularity': artist['popularity'],
        'spotify_url': artist['external_urls']['spotify'],
        'image_url': artist['images'][0]['url'] if artist['images'] else None
    }
    return artist_info


if __name__=='__main__':

    token = get_access_token()
    info = get_artist_info('Muse',token)
    print(info)