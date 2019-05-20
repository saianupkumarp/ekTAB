from flask import Blueprint, abort, jsonify, request, current_app, Response, send_file
from core import data
from datetime import datetime
from werkzeug.utils import secure_filename
import os, csv, io, ast, settings, uuid

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

@rest_api.route('/run_model', methods = ['POST'])
def run_model():
    if request.method == 'POST':
        if 'file' not in request.files:
            raise ErrorMessage('No files', status_code=503)
        input_file = request.files['file']
        if input_file.filename == '':
            raise ErrorMessage('No selected file', status_code=503)
        if input_file and data.allowed_file(input_file.filename):
            file_id = str(uuid.uuid4())
            input_file.save(os.path.join(settings.UPLOAD_PATH, 'csv', file_id + '.csv'))
        args = ast.literal_eval(request.form['data']) if request.form['data'] else ''
        result = data.run_task(file_id, args)
        return jsonify(result)

class ErrorMessage(Exception):
    status_code = 504

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv