from neo4j import GraphDatabase

host = 'bolt://localhost:11003'
user = 'neo4j'
password = 'password'
driver = GraphDatabase.driver(host, auth=(user,password))

def neo4j_query(query, params=None):
    with driver.session() as session:
        result = session.run(query, params)
        return [record.data() for record in result]

schema = neo4j_query('CALL apoc.meta.schema()')[0]['value']

'''
list[ # holds everything
    dict{ #relationship
        count:
        type:
        properties:
    }
    dict{ #nodes
        relationships:
        count:
        type:
        properties:
        labels:
    }
    .
    .
]
'''

filteredSchema = {}
for idx in schema:
    entity = schema[idx]
    fEntity = {}
    fEntity['type'] = entity['type']
    fEntity['properties'] = entity['properties']
    filteredSchema[idx] = fEntity



print(filteredSchema)