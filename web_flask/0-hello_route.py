#!/usr/bin/env python3
from flask import Flask
app = Flask(__name__)

# Define a route with strict_slashes=False
app.route('/', strict_slashes=False)

def hello():
    '''
    Hello Flask route
    '''
    return 'Hello HBNB!'

if __name__ == '__main__':
    # Run the app on 0.0.0.0, port 5000
    app.run(host='0.0.0.0', port=5000)

