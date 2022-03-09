from logging import debug
from flask import Flask, json, jsonify
from flask_cors import CORS
import os
from flask.helpers import send_file
import json


app = Flask(__name__)
CORS(app)
@app.route('/')
def root():
    return 'not the yattasss'

@app.route('/tierlist/')
def error():
    return 'invalid code'

@app.route('/tierlist/<id>')
def getList(id):
    if os.path.exists(f'api/{id}'):
        response = dict()
        with open(f'api/{id}/meta.json') as f:
            data = json.load(f)
            response['title'] = data['title']
            response['description'] = data['description']

        items = []
        for file in os.listdir(f'api/{id}'):
            if file != 'meta.json': 
                items.append(f'http://127.0.0.1:5000/tierlist/{id}/{file}')
        response['items'] = items
        
        return jsonify(response)
    else: return 'invalid code'

@app.route('/tierlist/<id>/<image>')
def getImage(id,image):
    return send_file(f'{id}\\{image}', mimetype='image/webp')

app.run(debug=True)