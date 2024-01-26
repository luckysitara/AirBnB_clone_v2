#!/usr/bin/python3
"""
ALX-AIRBONE_WEB_CLONE_FRAMEWORK
INTRODUCTION TO FLASK
"""

from flask import Flask

app = Flask(__name__)


@app.route('/airbnb-onepage/', strict_slashes=False)
def hbnb():
    '''
    Hello Flask route
    '''
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
