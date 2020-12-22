from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

import csv
from secret import client_id, client_secret

# Spotify API Object
# Note: Requires Client ID and Client Secret which is found from registering an app through Spotify's API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

"""
Playlist URI's:

Classes:
Jazz --> Jazz Classics, Coffee Table Jazz, Late Night Jazz, Smooth Jazz
Classical --> Classical Essentials, Calming Classical, Shimmering Strings, Classical Reading
Indie --> Ultimate Indie, Feel-Good Indie Rock, Lorem, Essential Indie
Country --> Hot Country, Tailgate Party, Big Country, Country Gold
Rock --> Rock Classics, Rock and Roll Party, Rock Hard, Rock This
Hip Hop --> Rap Caviar, Get Turnt, Most Necessary, Hip Hop Controller
EDM --> Mint, Dance Rising, Dance Hits, Trance Mission

"""
jazz_classics = 'spotify:playlist:37i9dQZF1DXbITWG1ZJKYt'
coffee_table_jazz = 'spotify:playlist:37i9dQZF1DWVqfgj8NZEp1'
late_night_jazz = 'spotify:playlist:37i9dQZF1DX4wta20PHgwo'
smooth_jazz = 'spotify:playlist:37i9dQZF1DXdwTUxmGKrdN'

jazz_playlists = [jazz_classics, coffee_table_jazz, late_night_jazz, smooth_jazz]

classical_essentials = 'spotify:playlist:37i9dQZF1DWWEJlAGA9gs0'
calming_classical = 'spotify:playlist:37i9dQZF1DWVFeEut75IAL'
shimmering_strings = 'spotify:playlist:37i9dQZF1DX2XWJkYVfE4v'
classical_reading = 'spotify:playlist:37i9dQZF1DWYkztttC1w38'

classical_playlists = [classical_essentials, calming_classical, shimmering_strings, classical_reading]

ultimate_indie = 'spotify:playlist:37i9dQZF1DX2Nc3B70tvx0'
feel_good_indie_rock = 'spotify:playlist:37i9dQZF1DX2sUQwD7tbmL'
lorem = 'spotify:playlist:37i9dQZF1DXdwmD5Q7Gxah'
essential_indie = 'spotify:playlist:37i9dQZF1DX26DKvjp0s9M'

indie_playlists = [ultimate_indie, feel_good_indie_rock, lorem, essential_indie]

hot_country = 'spotify:playlist:37i9dQZF1DX1lVhptIYRda'
tailgate_party = 'spotify:playlist:37i9dQZF1DXdgnLr18vPvu'
big_country = 'spotify:playlist:37i9dQZF1DXaJXCbmtHVHV'
country_gold = 'spotify:playlist:37i9dQZF1DWYnwbYQ5HnZU'

country_playlists = [hot_country, tailgate_party, big_country, country_gold]

rock_classics = 'spotify:playlist:37i9dQZF1DWXRqgorJj26U'
rock_and_roll_party = 'spotify:playlist:37i9dQZF1DWYE5MI4mMuii'
rock_hard = 'spotify:playlist:37i9dQZF1DWWJOmJ7nRx0C'
rock_this = 'spotify:playlist:37i9dQZF1DXcF6B6QPhFDv'

rock_playlists = [rock_classics, rock_and_roll_party, rock_hard, rock_this]

rap_caviar = 'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd'
get_turnt = 'spotify:playlist:37i9dQZF1DWY4xHQp97fN6'
most_necessary = 'spotify:playlist:37i9dQZF1DX2RxBh64BHjQ'
hip_hop_controller = 'spotify:playlist:37i9dQZF1DWT5MrZnPU1zD'

hip_hop_playlists = [rap_caviar, get_turnt, most_necessary, hip_hop_controller]

mint = 'spotify:playlist:37i9dQZF1DX4dyzvuaRJ0n'
dance_rising = 'spotify:playlist:37i9dQZF1DX8tZsk68tuDw'
dance_hits = 'spotify:playlist:37i9dQZF1DX0BcQWzuB7ZO'
trance_mission = 'spotify:playlist:37i9dQZF1DX91oIci4su1D'

edm_playlists = [mint, dance_rising, dance_hits, trance_mission]

# Get specified song features for all songs in a given playlist
def get_playlist_data(playlists, feature_list, label):
    data = []

    for playlist in playlists:
        # get track ID and track name from playlist
        tracks = sp.playlist_items(playlist, fields='items.track.id, items.track.name')

        for track in tracks['items']:
            if track['track'] != None:
                track_id = track['track']['id']
                # don't add duplicate songs
                if track_id not in (s[0] for s in data):
                    features = sp.audio_features(track_id)[0]
                    if features != None:
                        # extract specified features from Spotify track
                        sample = [features[ft] for ft in feature_list]
                        sample.insert(0, track_id)
                        sample.append(label)
                        data.append(sample)
                else:
                    print('Duplicate song found...')

    return data

if __name__ == '__main__':
    feature_list = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

    jazz_data = get_playlist_data(jazz_playlists, feature_list, 0)
    classical_data = get_playlist_data(classical_playlists, feature_list, 1)
    indie_data = get_playlist_data(indie_playlists, feature_list, 2)
    country_data = get_playlist_data(country_playlists, feature_list, 3)
    rock_data = get_playlist_data(rock_playlists, feature_list, 4)
    hip_hop_data = get_playlist_data(hip_hop_playlists, feature_list, 5)
    edm_data = get_playlist_data(edm_playlists, feature_list, 6)

    print('{} jazz songs extracted...'.format(len(jazz_data)))
    print('{} classical songs extracted...'.format(len(classical_data)))
    print('{} indie songs extracted...'.format(len(indie_data)))
    print('{} country songs extracted...'.format(len(country_data)))
    print('{} rock songs extracted...'.format(len(rock_data)))
    print('{} hip hop songs extracted...'.format(len(hip_hop_data)))
    print('{} edm songs extracted...'.format(len(edm_data)))

    hdr = feature_list
    hdr.insert(0, 'tid')
    hdr.append('label')

    with open('./data/data_5genre.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(hdr)
        csv_writer.writerows(jazz_data)
        csv_writer.writerows(classical_data)
        csv_writer.writerows(indie_data)
        csv_writer.writerows(country_data)
        csv_writer.writerows(rock_data)
        csv_writer.writerows(hip_hop_data)
        csv_writer.writerows(edm_data)
