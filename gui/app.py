from flask import Flask, render_template, request, flash

import os
from flask import send_from_directory


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
    propType = {
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
    return render_template('index.html', schema=schema, propType=propType)

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