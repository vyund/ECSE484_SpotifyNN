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
Study Music --> Deep Focus, Intense Studying, Classical Focus, Brain Food
Roadtrip Music --> Classic Road Trip, Feelin' Good, Dirt Road, Just Good Music
Workout Music --> Beast Mode, Pumped Pop , Workout Beats, Power Workout
Party Music --> Dance Rising, Dance Party, Floor Fillers, Mint
"""

deep_focus = 'spotify:playlist:37i9dQZF1DWZeKCadgRdKQ'
intense_studying = 'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6'
classical_focus = 'spotify:playlist:37i9dQZF1DXd5zUwdn6lPb'
brain_food = 'spotify:playlist:37i9dQZF1DWXLeA8Omikj7'

study_playlists = [deep_focus, intense_studying, classical_focus, brain_food]

classic_road_trip = 'spotify:playlist:37i9dQZF1DX9wC1KY45plY'
feelin_good = 'spotify:playlist:37i9dQZF1DX9XIFQuFvzM4'
dirt_road = 'spotify:playlist:37i9dQZF1DWTkxQvqMy4WW'
just_good_music = 'spotify:playlist:37i9dQZF1DX0b1hHYQtJjp'

roadtrip_playlists = [classic_road_trip, feelin_good, dirt_road, just_good_music]

beast_mode = 'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP'
pumped_pop = 'spotify:playlist:37i9dQZF1DX5gQonLbZD9s'
workout_beats = 'spotify:playlist:37i9dQZF1DWUSyphfcc6aL'
power_workout = 'spotify:playlist:37i9dQZF1DWUVpAXiEPK8P'

workout_playlists = [beast_mode, pumped_pop, workout_beats, power_workout]

dance_rising = 'spotify:playlist:37i9dQZF1DX8tZsk68tuDw'
dance_party = 'spotify:playlist:37i9dQZF1DXaXB8fQg7xif'
floor_fillers = 'spotify:playlist:37i9dQZF1DWWXrKtH3fzUd'
mint = 'spotify:playlist:37i9dQZF1DX4dyzvuaRJ0n'

party_playlists = [dance_rising, dance_party, floor_fillers, mint]

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

    study_data = get_playlist_data(study_playlists, feature_list, 0)
    roadtrip_data = get_playlist_data(roadtrip_playlists, feature_list, 1)
    workout_data = get_playlist_data(workout_playlists, feature_list, 2)
    party_data = get_playlist_data(party_playlists, feature_list, 3)

    print('{} study songs extracted...'.format(len(study_data)))
    print('{} roadtrip songs extracted...'.format(len(roadtrip_data)))
    print('{} workout songs extracted...'.format(len(workout_data)))
    print('{} party songs extracted...'.format(len(party_data)))

    hdr = feature_list
    hdr.insert(0, 'tid')
    hdr.append('label')

    with open('./data/data_4mood.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(hdr)
        csv_writer.writerows(study_data)
        csv_writer.writerows(roadtrip_data)
        csv_writer.writerows(workout_data)
        csv_writer.writerows(party_data)
