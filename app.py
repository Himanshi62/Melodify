import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, request
import model1 as m
from model1 import Data
import requests

app = Flask(__name__)

#.................client id for my app.....................................!
CLIENT_ID = '039b2470daf1402bad861d8c269c9314'

#.....................cliend scret id for my app..............................!
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



@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    req = requests.get(
        'https://api.spotify.com/v1/browse/new-releases', headers=headers)
    req = req.json()
    releases = []
    playlists = []
    for i in range(0, 11):
        arr_release = []
        arr_release.append(req['albums']['items'][i]['images'][0]['url'])
        arr_release.append(req['albums']['items'][i]
                           ['external_urls']['spotify'])
        releases.append(arr_release)
    for i in range(0, 10):
        r = requests.get(
            'https://api.spotify.com/v1/browse/featured-playlists?timestamp=2022-10-23T09%3A00%3A00.000Z', headers=headers)
        r = r.json()
        arr_play = []
        arr_play.append(r['playlists']['items'][i]['external_urls']['spotify'])
        arr_play.append(r['playlists']['items'][i]['images'][0]['url'])
        playlists.append(arr_play)
    return render_template("index.html", releases=releases, playlists=playlists)


@app.route('/predict1', methods=["POST"])
def predict1():
    if request.method == "POST":
        song = request.form["song"]
        num = 12
    result = m.make_matrix(Data, song, str(num))
    return render_template('recommend.html',  result=result, song=song, number=12)


@app.route('/predict2', methods=["POST"])
def predict2():
    if request.method == "POST":
        song = request.form["song"]
        num = 12

    result = m.make_matrix_cosine(Data, song, str(num))
    return render_template('recommend.html',  result=result, song=song, number=12)


@app.route('/predict3', methods=["POST"])
def predict3():
    if request.method == "POST":
        song = request.form["song"]
        num = 12

    result = m.make_matrix_correlation(Data, song, str(num))
    return render_template('recommend.html',  result=result, song=song, number=12)


@app.route('/predict4', methods=["POST"], endpoint='predict4')
def predict4():
    if request.method == "POST":
        id = request.form['id']
        artist = request.form['artist']
    tracks = []
    for i in range(0, 10):
        arr = []
        r = requests.get(BASE_URL + 'artists/' + id +
                         '/top-tracks' + '?market=US', headers=headers)
        r = r.json()
        arr.append(r['tracks'][i]['album']['images'][0]['url'])
        arr.append(r['tracks'][i]['album']['external_urls']['spotify'])
        arr.append(r['tracks'][i]['album']['name'])
        tracks.append(arr)

    return render_template('artist.html', tracks=tracks, artist=artist)


@app.route('/predict5', methods=["POST"])
def predict5():
    if request.method == "POST":
        id = request.form['id']
        artist = request.form['artist']
    tracks = []
    for i in range(0, 10):
        arr = []
        r = requests.get(BASE_URL + 'artists/' + id +
                         '/top-tracks' + '?market=US', headers=headers)
        r = r.json()
        arr.append(r['tracks'][i]['album']['images'][0]['url'])
        arr.append(r['tracks'][i]['album']['external_urls']['spotify'])
        arr.append(r['tracks'][i]['album']['name'])
        tracks.append(arr)

    return render_template('artist.html', tracks=tracks, artist=artist)


if __name__ == '__main__':
    app.run(debug=True)
