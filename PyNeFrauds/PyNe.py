from .extractor import extractSchema
from .Constructor import constructQueries

    
class PyNe():
    '''This class is a master controller/coordinator.
    It uses extractor.py to verify and extract the schema from jsonString.'''
    def __init__(self, jsonString):
        '''
        jsonString: A string following json format, the schema will be extracted from this.

        '''
        self.schema = extractSchema(jsonString)
        self.extractMetadata()
        self.constructQueries()
    
    def extractMetadata(self):
        '''From self.schema extracts following and sets as self. properties:
        # of nodes schema,
        list of types of nodes,'''
        self.numTypes = len(self.schema) #number of node types
        self.nodeTypes = [node['NodeLabel'] for node in self.schema]

    def constructQueries(self):
        '''From self.schema
        constructs CYPHER queries for fraud detection.'''
        self.queries = constructQueries(self.schema)
        return

    def showQueries(self):
        for node, nodeQueries in self.queries.items():
            print(f'\nNode: {node}')
            for level, query in nodeQueries.items():
                print(f'Level: {level}')
                print(query)




