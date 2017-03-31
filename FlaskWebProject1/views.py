"""
Routes and views for the flask application.
"""
import json
from flask import Flask, jsonify, render_template, request
from experience import Experience
from analytic import Analytic
from FlaskWebProject1 import APP

with open('./data/list_of_map.json') as data_json:
    MAP_DATA = json.load(data_json)

@APP.route('/', methods=['GET'])
def index():
    """The home route"""
    return render_template('home.html')

@APP.route('/findmap', methods=['POST'])
def level():
    """Get the map based on player's current level"""
    maps_analytic = Analytic(MAP_DATA)
    base_level = int(request.form['level'])
    experience = request.form['experience']

    if experience == 'full':
        filtered_map = maps_analytic.filter_by_exp(base_level, Experience.FULL)
    elif experience == 'ninetyfive':
        filtered_map = maps_analytic.filter_by_exp(base_level, Experience.NINETY_FIVE)
    elif experience == 'ninety':
        filtered_map = maps_analytic.filter_by_exp(base_level, Experience.NINETY)
    elif experience == 'over':
        filtered_map = maps_analytic.filter_by_exp(base_level, Experience.OVER)

    return render_template('map.html', map_data=filtered_map, base_level=base_level, experience=experience)
