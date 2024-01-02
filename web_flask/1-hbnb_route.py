#!/usr/bin/python3
"""
FIXING ROUTING
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
