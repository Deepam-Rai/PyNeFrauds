In this demo we will:
1. Use `demo_data_medical.csv` to populate neo4j database, using PyneFrauds.
2. Create embeddings of nodes in neo4j.
3. Add a target label `fraud` to some nodes for classification purpose.
4. We will fetch this embeddings from neo4j.
5. Convert this data to `torch_geometric` acceptable form.
6. Build a GNN model, train and evaluate.


----
# Dataset
This is just an example dataset containing entities:
1. Patient: name, age
2. Doctor: name, id
3. Problem: illness name

The relationships among them are:
1. (Patient)-[HAS]->(Problem)
2. (Patient)-[VISITS]->(Doctor)
3. (Doctor)-[TREATS]->(Problem)

The dataset looks like:
![Demo Dataset](Imagesataset.png)

----
# Populating neo4j
There are two ways to populate neo4j using PyneFrauds.
1. Each node and relationship type individually.
2. All nodes and relationship at once.

Way (1) is done in `demo_populating_neo4j_1.py`.  
Way (2) is done in `demo_populating_neo4j_2.py`.  

Both files are commented to explain the steps.

The populated neo4j database should look like:
![neo4j databse](Imageseo4j_database.png)

Irrespective of whichever way you populate, output is same.

----
# Embeddings
## Why embeddings?
We want to give our data to neural networks, but neural networks works with numbers only and our data can contain strings, dates, etc. Thus, we generate the embedding of our nodes/edges and provide this embedding to neural networks.  
There are [various in-built methods](https://neo4j.com/docs/graph-data-science/current/machine-learning/node-embeddings/) to generate embeddings given by default in neo4j. Below we use a very simple one without any fine-tuning.

## Unique identifier to nodes
This is required because there can be duplicate nodes and having a dedicated unique identifier makes work easier. **Pynefrauds requires unique ID for each node.**  
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
Official GDS guide [here](https://neo4j.com/docs/graph-data-science/current/).  
Plugins in neo4j-desktop:
![plugins](Imageslugins.png)

After installation their functions and methods can be used directly in neo4j browser.  

### Using FastRP
FastRP GDS guide [here](https://neo4j.com/docs/graph-data-science/current/machine-learning/node-embeddings/fastrp/).  
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

----
# Simple GNN classifier
To do so following steps are done:
1. Fetch the embeddings from neo4j.
2. Convert the embeddings, graph structure(nodes and relationships) to `torch_geometric` accepted form.
3. Build a classifier model.
4. Train the model.
5. Evaluate the model.

PyneFrauds makes all of these tasks one-liner.  
`demo_neural_classifier.py` file does this process and explains each step in comment.

The evaluation is available using Confusion Matrix only as of yet. Nevertheless since true_value and predicted_value are available any evaluation method can be manually used.

----
