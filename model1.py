import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.spatial import distance
import copy
import warnings
import requests
warnings.filterwarnings("ignore")
CLIENT_ID = '039b2470daf1402bad861d8c269c9314'
CLIENT_SECRET = 'b5aa0ef771084759a30e0b9e3a605aca'
AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']
BASE_URL = 'https://api.spotify.com/v1/'


#######################     Oauth token         ################################
headers = {
    'Authorization': 'Bearer BQAfCUokiL-PweRDa2fDsqglgKfzs-5-gxgEPxOU0snnme5lzOCOqzrvYwVaNXOk0iNyJuvAhOTo9rHAa5POIViaATTGA07K_vYqdhW8BpI6nBfMeY4kCyig5QZx6Asfl5wsJXOE0zLXJo3Sm-NvrRcYogbeyy3LXPE'.format(token=access_token)
}
##########################################################################



data = pd.read_csv("genres_v2.csv")


cols = list(data.columns[11:])
del cols[7]

df = copy.deepcopy(data)
df.drop(columns=cols, inplace=True)


df.head()


data = data.dropna(subset=['song_name'])


data.head()

data.shape


df = data[data.columns[:11]]


df.head()


df['genre'] = data['genre']

df.head()


df['time_signature'] = data['time_signature']
df['duration_ms'] = data['duration_ms']
df['song_name'] = data['song_name']
df['id'] = data['id']


x = df[df.drop(columns=['song_name', 'genre', 'id']).columns].values
scaler = StandardScaler().fit(x)
X_scaled = scaler.transform(x)
df[df.drop(columns=['song_name', 'genre', 'id']).columns] = X_scaled



Data = df


def find_word(word, words):
    t = []
    count = 0
    if word[-1] == ' ':
        word = word[:-1]
    for i in words:
        if word.lower() in i.lower():
            t.append([len(word)/len(i), count])
        else:
            t.append([0, count])
        count += 1
    t.sort(reverse=True)
    return words[t[0][1]]


################################# Engine1 ###################################

def make_matrix(data, song, number):
    df = pd.DataFrame()
    data.drop_duplicates(inplace=True)
    songs = data['song_name'].values
    best = find_word(song, songs)
    print('The song closest to your search is :', best)
    genre = data[data['song_name'] == best]['genre'].values[0]
    df = data[data['genre'] == genre]
    x = df[df['song_name'] == best].drop(
        columns=['genre', 'song_name', 'id']).values
    if len(x) > 1:
        x = x[1]
    song_names = df['song_name'].values
    df.drop(columns=['genre', 'song_name', 'id'], inplace=True)
    df = df.fillna(df.mean())
    p = []
    count = 0
    for i in df.values:
        p.append([distance.euclidean(x, i), count])
        count += 1
    p.sort()
    song_detail = []
    for i in range(1, int(number)+1):
        arr = []
        arr.append(song_names[p[i][1]])
        d = np.array(data[data['song_name'] == song_names[p[i][1]]]['id'])
        path = "https://open.spotify.com/track/" + d[0]
        arr.append(d[0])
        arr.append(path)
        r = requests.get(BASE_URL + 'tracks/' +
                         d[0] + '?market=ES', headers=headers)
        result = r.json()
        arr.append(result['artists'][0]['name'])
        arr.append(result['album']['images'][0]['url'])
        arr.append(result['duration_ms'])
        arr.append(result['album']['release_date'])
        arr.append(result['popularity'])
        arr.append(result['artists'][0]['id'])
        song_detail.append(arr)
        print(song_detail)
        song_detail.sort(key=lambda x: x[7], reverse=True)
    return song_detail


################################# Engine2 ###################################

def make_matrix_cosine(data, song, number):
    df = pd.DataFrame()
    data.drop_duplicates(inplace=True)
    songs = data['song_name'].values
    best = find_word(song, songs)
    print('The song closest to your search is :', best)
    genre = data[data['song_name'] == best]['genre'].values[0]
    df = data[data['genre'] == genre]
    x = df[df['song_name'] == best].drop(
        columns=['genre', 'song_name', 'id']).values
    if len(x) > 1:
        x = x[1]
    song_names = df['song_name'].values
    df.drop(columns=['genre', 'song_name', 'id'], inplace=True)
    df = df.fillna(df.mean())
    p = []
    count = 0
    for i in df.values:
        p.append([distance.cosine(x, i), count])
        count += 1
    p.sort()
    song_detail = []
    for i in range(1, int(number)+1):
        arr = []
        arr.append(song_names[p[i][1]])
        d = np.array(data[data['song_name'] == song_names[p[i][1]]]['id'])
        path = "https://open.spotify.com/track/" + d[0]
        arr.append(d[0])
        arr.append(path)
        r = requests.get(BASE_URL + 'tracks/' +
                         d[0] + '?market=ES', headers=headers)
        result = r.json()
        arr.append(result['artists'][0]['name'])
        arr.append(result['album']['images'][0]['url'])
        arr.append(result['duration_ms'])
        arr.append(result['album']['release_date'])
        arr.append(result['popularity'])
        arr.append(result['artists'][0]['id'])
        song_detail.append(arr)
        print(song_detail)
        song_detail.sort(key=lambda x: x[7], reverse=True)
    return song_detail


################################# Engine3 ###################################


def make_matrix_correlation(data, song, number):
    df = pd.DataFrame()
    data.drop_duplicates(inplace=True)
    songs = data['song_name'].values
    best = find_word(song, songs)
    print('The song closest to your search is :', best)
    genre = data[data['song_name'] == best]['genre'].values[0]
    df = data[data['genre'] == genre]
    x = df[df['song_name'] == best].drop(
        columns=['genre', 'song_name', 'id']).values
    if len(x) > 1:
        x = x[1]
    song_names = df['song_name'].values
    df.drop(columns=['genre', 'song_name', 'id'], inplace=True)
    df = df.fillna(df.mean())
    p = []
    count = 0
    for i in df.values:
        p.append([distance.correlation(x, i), count])
        count += 1
    p.sort()
    song_detail = []
    for i in range(1, int(number)+1):
        arr = []
        arr.append(song_names[p[i][1]])
        d = np.array(data[data['song_name'] == song_names[p[i][1]]]['id'])
        path = "https://open.spotify.com/track/" + d[0]
        arr.append(d[0])
        arr.append(path)
        r = requests.get(BASE_URL + 'tracks/' +
                         d[0] + '?market=ES', headers=headers)
        result = r.json()
        arr.append(result['artists'][0]['name'])
        arr.append(result['album']['images'][0]['url'])
        arr.append(result['duration_ms'])
        arr.append(result['album']['release_date'])
        arr.append(result['popularity'])
        arr.append(result['artists'][0]['id'])
        song_detail.append(arr)
        print(song_detail)
        song_detail.sort(key=lambda x: x[7], reverse=True)
    return song_detail
