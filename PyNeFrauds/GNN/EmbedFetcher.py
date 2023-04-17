from ..Globals import *
import numpy as np

class EmbedFetcher():
    def __init__(self, embedProperty, uniqueID=None, target=None):
        """
        Args:
            embedProperty (_type_): the property that contains embeddings
            uniqueID (_type_): property that is unique for every node. Defaults to None, in which case neo4j assigned <id> are used.
            target (_type_, optional): target value/ground truth property name. Defaults to None.
        """
        self.embedProperty = embedProperty
        self.uniqueID = uniqueID
        self.target = target
    
    def fetch_node_embeddings(self, nodeType=None):
        """Gets the node embedding of specified NodeType from the specified node embedding property.

        Args:
            nodeType (str, optional): Specific node type of which embeddings are required. 
                Defaults to None and extracts for all node type(Assuming all node types have self.embedProperty as their property).
        Returns:
            list: Result of CYPHER query executed on neo4j.
        """
        query = f'MATCH (n{"" if nodeType is None else ":"+nodeType}) \
            RETURN {"id(n)" if self.uniqueID is None else "n."+self.uniqueID} as {"Neo4jID" if self.uniqueID is None else self.uniqueID}, \
              labels(n) as Label, n.{self.embedProperty} as {self.embedProperty}, n.{self.target} as {self.target}'
        result = neo4jHandler.query(query)
        self.embeddings = result
        return result



    def set_ref_indexes(self):
        """Assigns a unique integer to all the nodes. 
        This integers form the index of this nodes in the feature matrix and same is used to indicate nodes in COO edge matrix too.

        Returns:
            dict: {"unique_id":"index"}
        """
        self.REF_INDEX = {}
        for i, node in enumerate(self.embeddings):
            self.REF_INDEX[node[self.uniqueID]] = i
        return self.REF_INDEX



    def fetch_feature_matrix(self):
        '''Fetches feature matrix from neo4j and also sets as own property.
        id: id that uniquely identifies every node. Should be present in REF_INDEX; these are taken as nodes
        propertyName: Dictionary key in which the embedding is saved as list; these are taken as features
        embeddings: List of Dictionaries with necessary two keys in dictionary;
                    i) id
                    ii) propertyName
        returns: (num nodes)x(num features) numpy matrix
        '''
        self.featureMatrix = np.zeros((len(self.embeddings), len(self.embeddings[0][self.embedProperty])))
        for node in self.embeddings:
            self.featureMatrix[ self.REF_INDEX[node[self.uniqueID]]] = np.array(node[self.embedProperty])
        return self.featureMatrix


    def fetch_edge_COO(self,relationName=None, sourceProperty='project_id', destProperty='project_id'):
        '''relationName: If None then gets for all kind of relationships.
        sourceProperty: Source node identifier. Should be part of REF_INDEX
        nodeProperty: Destination node identifier. Should be part of REF_INDEX
        Querer: QueryEx object that executes queries
        These two are basically to know from which node to which node relation is connecting.
        Returns a list of [source,destination] pairs for that relation as numpy.ndarray
        '''
        query = f'MATCH (n)-[r{"" if relationName is None else ":"+relationName}]->(m) RETURN  COLLECT([n.{sourceProperty} , m.{destProperty}]) as edge'
        result = neo4jHandler.query(query)
        unprocessed = result[0]['edge']
        processed = [[self.REF_INDEX[x[0]],self.REF_INDEX[x[1]]] for x in unprocessed]
        self.edge_index = processed
        return processed


    def set_targets(self):
        '''Returns: target values - corresponding to the self.fraudLabel
        '''
        if self.target is None:
            return None
        targets = np.zeros(len(self.embeddings))
        for node in self.embeddings:
            targets[ self.REF_INDEX[node[self.uniqueID]]] = np.array(node[self.target])
        return targets


    def fetchData(self,nodeType=None, relName=None,):
        """Fetches the embeddings from neo4j. Transforms into feature matrix, edge index, targets form and sends back.

        Args:
            nodeType (str, optional): Specific nodeType only which needs to be present in feature matrix. 
                    Defaults to None, fetches for all nodes(Assuming all nodeTypes possess {self.embedProperty}).
            relName (str, optional): Specific relation only which needs to be formed edge index.
                     Defaults to None, fetches all relations in COO format.

        Returns:
            self.REF_INDEX, self.featureMatrix, self.edge_index, targets
        """
        #get embeddings and target
        self.fetch_node_embeddings(nodeType=nodeType)
        #get new references
        self.set_ref_indexes()
        #get feature matrix
        self.fetch_feature_matrix()
        #get coo edge-index
        self.fetch_edge_COO(relationName=relName, sourceProperty=self.uniqueID, destProperty=self.uniqueID)
        #get targets
        targets = self.set_targets()

        return self.REF_INDEX, self.featureMatrix, self.edge_index, targets
