from ..Globals import *
import numpy as np
# import torch

class EmbedFetcher():
    def __init__(self, embedProperty, uniqueID=None, target=None):
        """
        Warning: If uniqueID value is provided and the property doesn't exist in neo4j, then some junk value will be returned.
        Args:
            embedProperty (str): the property that contains embeddings
            uniqueID (str): property that is unique for every node. Defaults to None, in which case neo4j assigned <id> are used.
            target (str, optional): target value/ground truth property name. Defaults to None.
        """
        self.embedProperty = embedProperty
        self.uniqueID = uniqueID
        self.target = target
    
    def fetch_node_embeddings(self, nodeType=None):
        """Gets the node embedding of specified NodeType from the specified node embedding property from neo4j.
        If uniqueID is set to None, then uses neo4j assigned unique id as primary key to identify nodes and
            sets self.uniqueID as 'Neo4jID'.

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
            self.REF_INDEX[node[ "Neo4jID" if self.uniqueID is None else self.uniqueID]] = i
        return self.REF_INDEX



    def fetch_feature_matrix(self):
        """Fetches the self.embedProperty values for all nodes from neo4j.  
            Sets the fetched feature matrix as self.featureMatrix in tensor form.

        Returns:
            numpy.ndarray: feature matrix 
        """
        featureMatrix = np.zeros((len(self.embeddings), len(self.embeddings[0][self.embedProperty])))
        uniqueID = "Neo4jID" if self.uniqueID is None else self.uniqueID
        for node in self.embeddings:
            featureMatrix[ self.REF_INDEX[node[uniqueID]]] = np.array(node[self.embedProperty])
        self.featureMatrix = featureMatrix #torch.tensor(featureMatrix, dtype=torch.float)
        return featureMatrix


    def fetch_edge_COO(self,relationName=None, sourceProperty='project_id', destProperty='project_id'):
        """Fetches the 'relationName' relations from neo4j database. Converts into COO edge_index.
        Sets self.edge_index as fetched edge_COO in tensor form. 

        Args:
            relationName (_type_, optional): _description_. Defaults to None.
            sourceProperty (str, optional): _description_. Defaults to 'project_id'.
            destProperty (str, optional): _description_. Defaults to 'project_id'.

        Returns:
            _type_: _description_
        """
        query = f'MATCH (n)-[r{"" if relationName is None else ":"+relationName}]->(m) \
            RETURN  COLLECT({ "[id(n),id(m)]" if self.uniqueID is None else "[n." +self.uniqueID+" , m."+self.uniqueID+"]"}) as edge'
        result = neo4jHandler.query(query)
        unprocessed = result[0]['edge']
        processed = [[self.REF_INDEX[x[0]],self.REF_INDEX[x[1]]] for x in unprocessed]
        self.edge_index = processed #torch.tensor(processed, dtype=torch.long)
        return processed


    def set_targets(self):
        """From self.embeddings sets the self.targets. sets to None if self.target is None.
            self.targets are the values of the property with name {self.targets} in neo4j database.
        Returns:
            self.targets
        """
        if self.target is None:
            self.targets=None
            return None
        self.targets = np.zeros(len(self.embeddings))
        for node in self.embeddings:
            self.targets[ self.REF_INDEX[node["Neo4jID" if self.uniqueID is None else self.uniqueID]]] = np.array(node[self.target])
        return self.targets


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
        self.set_targets()

        return self.REF_INDEX, self.featureMatrix, self.edge_index, self.targets
