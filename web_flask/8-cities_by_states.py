#!/usr/bin/python3
"""
This module provides flask app routing certain view pages.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def state_list():
    states_list = storage.all(State)
    sorted_list = sorted(states_list.values(), key=lambda s: s.name)
    return render_template('7-states_list.html', states_list=sorted_list)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_state_list():
    states_list = storage.all(State)
    sorted_list = sorted(states_list.values(), key=lambda s: s.name)
    return render_template('8-cities_by_states.html', states_list=sorted_list)


@app.teardown_appcontext
def teardown_db(exception=None):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
