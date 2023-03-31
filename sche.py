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

for idx in schema:
    entity = schema[idx]
    if entity['type']=='relationship':
        count, type, properties = entity.values()
        print(properties.keys())
    elif entity['type']=='node':
        relationships, count, type, properties, labels = entity.values()
        print(properties.keys())
