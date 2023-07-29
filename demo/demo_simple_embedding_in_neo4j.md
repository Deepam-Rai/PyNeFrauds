Graph Created:  


## Why embeddings?
We want to give our data to neural networks, but neural networks works with numbers only and our data can contain strings, dates, etc. Thus we generate the embedding of our nodes/edges and provide this embedding to neural networks.  
There are various in-built methods to generate embeddings given by default in neo4j. Below we use a very simple one without any fine-tuning.

## Unique identifier to nodes
This is required because there can be duplicate nodes and having a dedicated unique identifier makes work easier. Pynefrauds requires unique ID for each node.  
Unique ID can be given as per one's own logic. Below we use neo4j's by default assigned unique ID.  
Setting a new attribute constraint for all nodes:
```cypher
CREATE CONSTRAINT FOR (n:Label) REQUIRE n.unique_id is UNIQUE
```
Setting the default neo4j assigned IDs to the nodes as their unique identifier:
```cypher
MATCH (n) SET n.unique_id = id(n)
```

## Getting embeddings
The methods are provided as plugins, called GDS(Graph Data Science) library for neo4j-desktop. They need to be installed for each neo4j database where you want to use them.  
Official GDS guide: https://neo4j.com/docs/graph-data-science/current/  
After installation their functions and methods can be used directly in neo4j browser.  

### Using FastRP
Projecting the graph:
```CYPHER
CALL gds.graph.project(
	'projected_graph',
	'*',
	'*'
)
```
Getting embeddings and saving as a new property(`fastRP_embedding`):
```CYPHER
CALL gds.fastRP.write(
	'projected_graph',
	{
		writeProperty:'fastRP_embedding',
		embeddingDimension:7,
		iterationWeights:[3.0,1.0],
		nodeSelfInfluence:1.0,
		randomSeed:13
	}
)
```

## Crating fraud labels
For the sake of demo we will create a new property - `fraud` for all nodes with value `0` as not being fraud. We will set it to `1` as being fraud and then build a neural network classifier to predict the fraudlent nodes.  

Setting a fraud property for all nodes:
```CYPHER
MATCH (n) set n.fraud = 0
```
Setting some patients as frauds:
```CYPHER
MATCH(n:Patient)
WHERE n.patient_name = 'Sonali' OR  n.patient_name='Inaya' OR n.patient_name = 'Mihir' OR n.patient_name = 'Tenzin'

SET n.fraud = 1
```