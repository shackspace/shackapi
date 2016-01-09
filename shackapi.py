#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
import json
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/portal/status')
def portal_status():
    response = requests.get('http://portal.shack:8088/status').json()
    return jsonify(response) 

@app.route('/mpd/toggle')
def mpd_toggle():
    from mpd import MPDClient
    client = MPDClient()
    client.connect('mpd.shack', 6600)
    state = client.status()['state']
    if state == 'play':
        client.pause()
        new_state = 'pause'
    else:
        client.play()
        new_state = 'play'

    client.close()
    client.disconnect()
    response = jsonify({'old_state': state,
                 'new_state': new_state})
    return response 

@app.route('/mpd/song')
def mpd_song():
    from mpd import MPDClient
    client = MPDClient()
    client.connect('mpd.shack', 6600)
    song = client.currentsong()
    print(song)
    client.close()
    client.disconnect()
    return jsonify(song)

if __name__ == "__main__":
        app.debug = True
        app.run(host='::')
