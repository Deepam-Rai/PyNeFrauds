from PyNeFrauds.Globals import neo4jHandler
from PyNeFrauds.nn import EmbedFetcher, PyGDataWrapper

from collections import OrderedDict
from PyNeFrauds.nn import NNModel, train, ConfusionMatrix
import torch_geometric.nn as tgnn
import torch.nn as tnn

print("Setting up the neo4j handler...")
host = 'bolt://localhost:7687'
user = "neo4j"
password = "password"


print("Setting neo4j credentials...")
neo4jHandler.set_credentials(host,user,password)

# set the parameters for fetching
embedFetcher = EmbedFetcher(
    embedProperty="fastRP_embedding",  # neo4j property that has embeddings
    uniqueID='unique_id',   # unique ID assigned to every node in database
    target="fraud"          # target property for classification
)

print("Fetching the embeddings from neo4j...")
embedFetcher.fetchData()

# create torch_geometric acceptable format
dWrap = PyGDataWrapper()   # this object will convert the neo4j data to torch-geometric accepted data
dWrap.from_embed_fetcher(embedFetcher)   # converts the data
dWrap.set_train_mask(frac=0.2)    # GNN can use train-masks for better performance

print("\nDetails of fetched data:")
dWrap.show_data_info()


print("\nNN model:")
modules = OrderedDict({            #define the layers of model
    'GCN1' : tgnn.GCNConv(7, 16),
    'relu1': tnn.ReLU(),
    'linear': tnn.Linear(16,2),
    'softmax': tnn.Softmax(dim=1)
})
model = NNModel(modules=modules)  #instantiate the model
print(model)

print("\nTraining NN model...")
model, losses = train(model=model, data=dWrap.data, n_epoch=5, print_interval=1)

print("\nEvaluating trained model:")
ConfusionMatrix(model=model, data=dWrap.data, use_test_mask=True, saveFig="")
