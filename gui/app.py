from flask import Flask, render_template, request, flash, jsonify

import os
from flask import send_from_directory

from connector import gui_input_to_schema

app = Flask(__name__)

@app.route('/')
def index():
    # fetch the schema of the graph
    schema = {
        'Relationships':{
            'RelType1':{
                'prop1':{
                    'type':'int',
                    'value':1
                },
                'prop2':2
            },
            'RelType1':{
                'prop1':{
                    'type':'int',
                    'value':1
                },
                'prop2':{
                    'type':'int',
                    'value':1
                },
                'prop3':{
                    'type':'int',
                    'value':1
                }
            }
        },
        'Nodes':{
            'nodeType1':{
                'prop1':{
                    'type':'int',
                    'value':1
                },
                'prop2':{
                    'type':'str',
                    'value':'someString'
                }
            },
            'Patient':{
                'Name':{
                    'type':'str',
                    'value':'Adam'
                },
                'prop2':{
                    'type':'int',
                    'value':1
                },
                'prop3':{
                    'type':'list',
                    'value': ['Male','Female','Other']
                }
            }

        }
    }
    #fetch constraints
    propConstrMap = {
        'int' : {
            'constraint':'range',
            'prefixes' : ['IS','IS NOT']
        },
        'str' : {
            'constraint':'regex',
            'prefixes' : ['IS OF','IS NOT OF']
        },
        'list': {
            'constraint':'list',
            'prefixes' : ['IN','NOT IN']
        },
    }
    return render_template('index.html', schema=schema, propConstrMap=propConstrMap)

@app.route('/create_query', methods=['POST'])
def create_query():
    form_data = request.form #get the form data
    #process the form data
    result = gui_input_to_schema(form_data)
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

if __name__=='__main__':
    app.run(debug=True, port=8008)