from flask import Flask, render_template, request, flash, jsonify

import os
from flask import send_from_directory

from schema_fetcher import NeoQuerer
from connector import gui_input_to_schema

app = Flask(__name__)

host = 'bolt://localhost:11003'
user = "neo4j"
password = "password"
querer = NeoQuerer(host, user,password)


@app.route('/')
def index():
    # fetch constraints
    propConstrMap = {
        'INTEGER': {
            'constraint': 'range',
            'prefixes': ['IS', 'IS NOT']
        },
        'FLOAT': {
            'constraint': 'range',
            'prefixes': ['IS', 'IS NOT']
        },
        'STRING': {
            'constraint': 'regex',
            'prefixes': ['IS OF', 'IS NOT OF']
        },
        'LIST': {
            'constraint': 'list',
            'prefixes': ['IN', 'NOT IN']
        },
    }
    # fetch the schema of the graph
    schema = querer.get_processed_schema()
    return render_template('index.html', schema=schema, propConstrMap=propConstrMap)


@app.route('/create_query', methods=['POST'])
def create_query():
    input_data = request.get_json()  # get the form data
    # process the form data
    result = gui_input_to_schema(input_data)
    return jsonify(result)


@app.route('/neo4jLogin')
def neo4j_login():
    return render_template('neo4j_login.html')


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')


if __name__ == '__main__':
    app.run(debug=True, port=8008)
