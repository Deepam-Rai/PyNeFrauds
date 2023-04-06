from flask import Flask, render_template, request, flash, jsonify

import os
from flask import send_from_directory

from schema_fetcher import NeoQuerer
from connector import gui_input_to_schema

app = Flask(__name__)

querer = NeoQuerer(host=None, user=None, password=None)
# querer = NeoQuerer(host='bolt://localhost:11003', user='neo4j', password='password')


@app.route('/gui_cypher')
def gui_cypher():
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
    schema = None
    if querer.host==None or querer.user==None:
        logIn = {'value':False}
        schema = {}
    else:
        logIn = {'value':True}
        schema = querer.get_processed_schema()
    return render_template('gui_cypher.html',logIn=logIn, schema=schema, propConstrMap=propConstrMap)


@app.route('/create_query', methods=['POST'])
def create_query():
    if querer.host==None or querer.user==None:
        return jsonify({"CYPHER":"Login into Neo4j First."})
    input_data = request.get_json()  # get the form data
    # process the form data
    result = gui_input_to_schema(input_data)
    return jsonify(result)


@app.route('/neo4j_login')
def neo4j_login():
    return render_template('neo4j_login.html')


@app.route('/validateCredentials', methods=['POST'])
def validate_credentials():
    host = request.json.get('host')
    username = request.json.get('username')
    password = request.json.get('password')

    print(host)
    querer.setCredentials(host=host, user=username,password=password)
    if querer.validateCredentials():
        # Credentials are valid, return a success message
        return jsonify({'success': True}), 200
    else:
        # Credentials are invalid, return an error message
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401


@app.route('/form')
def form():
    return render_template('visualizer.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')

@app.route('/')
def index():
    return neo4j_login()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8008)
