#!/usr/bin/python3
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    '''
    Hello Flask route
    '''
    return 'Hello HBNB!'

    app.run(host='0.0.0.0, port=5000)
    app.url_map.strict_slashes = False
