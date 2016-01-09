#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
import json
import requests

app = Flask(__name__)
mpd_room_to_port = {'lounge': 6600,
                    'semi': 6601,
                    'elab': 6602,
                    'kueche': 6603,
                    'crafting': 6604,
                    'fablab': 6605,
                    'workshop': 6606}

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/portal/status')
def portal_status():
    response = requests.get('http://portal.shack:8088/status').json()
    return jsonify(response) 

@app.route('/mpd/<string:room>/status')
def mpd_status(room):
    if not room in mpd_room_to_port:
        return jsonify({'error': 'unkown room'})
    from mpd import MPDClient
    client = MPDClient()
    client.connect('mpd.shack', mpd_room_to_port[room])
    state = client.status()['state']
    return jsonify({'status': state})

@app.route('/mpd/<string:room>/toggle')
def mpd_toggle(room):
    if not room in mpd_room_to_port:
        return jsonify({'error': 'unkown room'})
    from mpd import MPDClient
    client = MPDClient()
    client.connect('mpd.shack', mpd_room_to_port[room])
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

@app.route('/mpd/<string:room>/song')
def mpd_song(room):
    if not room in mpd_room_to_port:
        return jsonify({'error': 'unkown room'})
    from mpd import MPDClient
    client = MPDClient()
    client.connect('mpd.shack', mpd_room_to_port[room])
    song = client.currentsong()
    client.close()
    client.disconnect()
    return jsonify(song)

@app.route('/trash/dates')
def trash_date():
    resp = {}
    r = requests.get("https://meinsack.click/v1/70327/Ulmer%20Stra%C3%9Fe/")
    resp['next_yellow'] = r.json().get('dates')[0]
    return jsonify(resp)

if __name__ == "__main__":
        app.debug = True
        app.run(host='::')
