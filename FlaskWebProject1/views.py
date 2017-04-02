"""
Routes and views for the flask application.
"""
import json
from flask import Flask, jsonify, render_template, request
from experience import ExpRate, ExpTable
from analytic import Analytic
from FlaskWebProject1 import app

with open('FlaskWebProject1/data/list_of_map.json') as data_json:
    MAP_DATA = json.load(data_json)

@app.route('/', methods=['GET'])
def index():
    """The home route"""
    return render_template('home.html')

@app.route('/findmap', methods=['POST'])
def level():
    """Get the map based on player's current level"""
    maps_analytic = Analytic(MAP_DATA)
    base_level = int(request.form['level'])
    experience = request.form['experience']

    lvl_row = [row for row in ExpTable.BASE if row[0] == base_level]
    next_exp = lvl_row[0][2]

    if experience == '1':
        filtered_map = maps_analytic.classic_exp_filter(base_level, ExpRate.HUGE)
    elif experience == '2':
        filtered_map = maps_analytic.classic_exp_filter(base_level, ExpRate.LARGE)
    elif experience == '3':
        filtered_map = maps_analytic.classic_exp_filter(base_level, ExpRate.SMALL)
    elif experience == '4':
        filtered_map = maps_analytic.classic_exp_filter(base_level, ExpRate.LITTLE)
    elif experience == '5':
        filtered_map = maps_analytic.classic_exp_filter(base_level, ExpRate.SAD)
    elif experience == '6':
        filtered_map = maps_analytic.classic_exp_filter(base_level, ExpRate.MODERATE)

    return render_template('map.html', map_data=filtered_map, base_level=base_level, experience=experience, next_exp=next_exp)
