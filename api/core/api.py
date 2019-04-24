from flask import Blueprint, abort, jsonify, request, current_app, Response, send_file
from core import data
from datetime import datetime
import os

#Rest API
rest_api = Blueprint('rest_api', __name__)

@rest_api.route('/status')
def get_config():
    return "Success API"

@rest_api.route('/get_line_data')
def get_actors():
    DATABASE = '/Users/anupkumar/Documents/Projects/KAPSARC/KTAB/examples/smp/doc/AK_Large.db'
    # filters = {'scenarioID': "000000000000000040BAC5BE3D1236F1", "dimID": 0}
    dat = data.get_data(DATABASE, 'LineChartQuery')
    return jsonify(dat)

