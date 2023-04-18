# from PyNeFrauds.Globals import neo4jHandler
import PyNeFrauds.QueryConstructor as QueryConstructor
from PyNeFrauds.nn import EmbedFetcher
from PyNeFrauds.nn import PyGDataWrapper
from PyNeFrauds.nn import NNModel
from PyNeFrauds.nn import train, ConfusionMatrix

import torch.nn as tnn
import torch_geometric.nn as tgnn

from collections import OrderedDict
# from PyNeFrauds.Constructor import testFun
# from PyNeFrauds.extractor import verifyAttributeProperties


# Query Constructor
json_text = '''
[{
  "NodeLabel" : "Patient",
  "ref" : "n0",
  "type" : "node",
  "Attributes" : [
    ["Name", "IS NOT OF", "w"],
    ["Contact", "IS", {">" : 9999999999}],
    ["Age", "IS NOT", {"<=":130}],
    ["asdf", "IS", {"<":23, ">=":"n1.Cost"}],
    ["ID", "IS NOT", {"<":0}],
    ["Gender", "NOT IN", ["Male","Female","Others"]]
  ],
  "NodeProperties" : {}
},
{
  "NodeLabel" : "Treatment",
  "ref" : "n1",
  "type" : "node",
  "Attributes" : [
    ["Name", "IS OF", "w"],
    ["Cost", "IS", {"=":5000}],
    ["asdf", "IS", {"<":23, ">=":14}],
    ["ID", "IS", {"<":0}],
    ["Category", "IN", ["Oncology","Pediatrics"]]
  ],
  "NodeProperties" : {}
}]
'''

# Generating queries
# print(PyNeFrauds.Globals.neo4jHandler.get_credentials())

# cone = QueryConstructor(json_text)
# print(cone.queries)
# print(cone.queries['Patient'][1])
# cone.constructQueries(mode='MERGED')
# cone.showQueries()

# neo4j credentials
src.Globals.neo4jHandler.set_credentials("bolt://localhost:11003", "neo4j","password")

# fetching embeddings from neo4j
x = src.nn.EmbedFetcher(embedProperty="fastRP", uniqueID=None, target="fraud")
REF_INDEX, featureMatrix, edge_index, targets = x.fetchData()
# print(x.fetch_node_embeddings()[0])

# creating torch_geometric data
dWrap = PyGDataWrapper()
dWrap.from_embed_fetcher(x, frac=0.2)
dWrap.show_data_info()
# print(edge_index)

# Building GNN model
modules = OrderedDict({
    'GCN1' : tgnn.GCNConv(7, 30),
    'drop0': tnn.Dropout(p=0.5),
    'relu1': tnn.ReLU(),
    'GCN2' : tgnn.GCNConv(30, 40),
    'relu1': tnn.ReLU(),
    'linear': tnn.Linear(40,512),
    'relul1': tnn.ReLU(),
    'drop1': tnn.Dropout(p=0.2),
    'linear2': tnn.Linear(512,2),
    'softmax': tnn.Softmax(dim=1)
})

#building usual NN model
input_dim=7
hidden_dim=128
output_dim=2
modules2 = OrderedDict({
      'Linear1': tnn.Linear(input_dim, hidden_dim),
      'relu1':tnn.ReLU(),
      'Linear2':tnn.Linear(hidden_dim, output_dim),
      'softmax':tnn.Softmax(dim=1)
})
model = NNModel(modules=modules)
print(model)

# Training model
train(model=model, data=dWrap.data, n_epoch=601, print_interval=30)

# Evaluating using confusion matrix
ConfusionMatrix(model=model, data=dWrap.data, use_test_mask=True, saveFig="")
