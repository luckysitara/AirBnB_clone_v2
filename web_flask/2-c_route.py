#!/usr/bin/python3
'''
ADDIING ESCAPE TO ROUTING
'''


from flask import Flask, escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    '''
    return hello_hbnb function
    '''

    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''
    function for hbnb
    '''

    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    '''
    function for c_route
    '''

    return "C  {}".format(escape(text.replace('_', ' ')))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
