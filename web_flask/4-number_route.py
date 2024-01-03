#!/usr/bin/python3
"""
This script starts a Flask web application with specific routes.
"""

from flask import Flask, render_template

app = Flask(__name__)

# Route to display 'Hello HBNB!'


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!'"""
    return 'Hello HBNB!'


# Route to display 'HBNB'
@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display 'HBNB'"""
    return 'HBNB'


# Route to display 'C' followed by the value of the text variable
@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Display 'C' followed by the value of the text variable"""
    return 'C {}'.format(text.replace('_', ' '))

# Route to display 'Python' followed by the value of the text variable
# Default value for text is 'is cool'


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python/', strict_slashes=False, defaults={'text': 'is cool'})
def python_text(text):
    """Display 'Python' followed by the value of the text variable"""
    return 'Python {}'.format(text.replace('_', ' '))

# Route to display 'n is a number' only if n is an integer


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Display 'n is a number' only if n is an integer"""
    return '{} is a number'.format(n)

# Run the application on 0.0.0.0:5000


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
