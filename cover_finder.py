import requests
import os

def find_album_cover_itunes(search_query):
    url = f"https://itunes.apple.com/search?term={search_query}&entity=album&limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['resultCount'] > 0:
            album_cover_url = data['results'][0]['artworkUrl100'].replace('100x100', '600x600')
            return album_cover_url
    return None

def find_album_cover_lastfm(search_query):
    api_key = 'YOUR_LASTFM_API_KEY'  # Replace with your Last.fm API key
    url = f"http://ws.audioscrobbler.com/2.0/?method=album.search&album={search_query}&api_key={api_key}&format=json&limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and 'albummatches' in data['results'] and 'album' in data['results']['albummatches']:
            albums = data['results']['albummatches']['album']
            if albums:
                album_cover_url = albums[0]['image'][-1]['#text']  # Get the largest image
                return album_cover_url
    return None

def download_album_cover(song_name, save_path='covers'):
    search_query = os.path.splitext(os.path.basename(song_name))[0]
    album_cover_url = find_album_cover_itunes(search_query) or find_album_cover_lastfm(search_query)
    if album_cover_url:
        response = requests.get(album_cover_url)
        if response.status_code == 200:
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            cover_path = os.path.join(save_path, f"{search_query}.jpg")
            with open(cover_path, 'wb') as f:
                f.write(response.content)
            return cover_path
    else:
        print(f"No album cover found for song: {song_name}")
    return 'Icons/vinyl.png'  # Replace with the path to your stock image