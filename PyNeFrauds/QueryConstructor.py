from .Globals import *
from .extractor import extractSchema
from .Constructor import constructQueries, all_in_one_query

import json
    
class QueryConstructor():
    '''This class is a master controller/coordinator.
    It uses extractor.py to verify and extract the schema from jsonString.'''
    def __init__(self, jsonString):
        '''
        jsonString: A string following json format, the schema will be extracted from this.

        '''
        self.schema = extractSchema(jsonString, verify=False)
        self.extractMetadata()
        self.constructQueries()
    
    def extractMetadata(self):
        '''From self.schema extracts following and sets as self. properties:
        # of nodes schema,
        list of types of nodes,'''
        self.numTypes = len(self.schema) #number of node types
        self.nodeTypes = [node['NodeLabel'] for node in self.schema]

    def constructQueries(self, mode="INDIVIDUAL"):
        '''From self.schema
        constructs CYPHER queries for fraud detection.'''
        if mode=="INDIVIDUAL":
            self.queries = constructQueries(self.schema)
        elif mode=="MERGED":
            self.queries = all_in_one_query(self.schema)
        return

    def showQueries(self):
        if isinstance(self.queries, dict):
            for node, nodeQueries in self.queries.items():
                print(f'\nNode: {node}')
                for level, query in nodeQueries.items():
                    print(f'Level: {level}')
                    print(query)
        else:
            print(self.queries)




