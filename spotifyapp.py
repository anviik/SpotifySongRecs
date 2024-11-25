import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#api
SPOTIFY_CLIENT_ID = "c66eaee4bb3f4798988720d566a3e603"
SPOTIFY_CLIENT_SECRET = "81adb766d0494daf944e87d90643a5a4"

credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=credentials_manager)

def fetch_album_cover(song_title, artist_name):
    query = f"track:{song_title} artist:{artist_name}"
    search_results = spotify.search(q=query, type="track")

    if search_results and search_results["tracks"]["items"]:
        first_track = search_results["tracks"]["items"][0]
        album_cover_url = first_track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def suggest(selected_song):
    song_index = music_data[music_data['song'] == selected_song].index[0]
    sorted_distances = sorted(enumerate(similarity_matrix[song_index]), key=lambda x: x[1], reverse=True)
    
    recommended_songs = []
    album_covers = []

    for entry in sorted_distances[1:6]:
        recommended_artist = music_data.iloc[entry[0]].artist
        recommended_song = music_data.iloc[entry[0]].song
        print(recommended_artist, recommended_song)
        
        album_covers.append(fetch_album_cover(recommended_song, recommended_artist))
        recommended_songs.append(recommended_song)

    return recommended_songs, album_covers


st.title('Music Recommendation System')

# load data
music_data = pickle.load(open('df.pkl', 'rb'))
similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))

# dropdown 
available_songs = music_data['song'].values
chosen_song = st.selectbox("Search for a song from the list below:", available_songs)

# display recommendations upon button click
if st.button('Get Recommendations'):
    recommendations, covers = suggest(chosen_song)
    
    columns = st.columns(5)
    for idx, col in enumerate(columns):
        with col:
            st.text(recommendations[idx])
            st.image(covers[idx])
