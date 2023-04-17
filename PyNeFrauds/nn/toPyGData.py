import torch
from torch_geometric.data import Data

class PyGData():
    def __init__(self, featureMatrix=None, edge_index=None, targets=None ):
        """Class that wraps the torch_geometric.data.Data for this library.
        Aim is to make handling, manipulating torch_geometric accepted data easy.

        Args:
            featureMatrix (_type_, optional): _description_. Defaults to None.
            edge_index (_type_, optional): _description_. Defaults to None.
            targets (_type_, optional): _description_. Defaults to None.
        """
        featureMatrix = None if featureMatrix is None else torch.tensor(featureMatrix, dtype=torch.float)
        edge_index = None if edge_index is None else torch.tensor(edge_index, dtype=torch.long)
        # ty = torch.tensor([[1,0] if x==0 else [0,1] for x in targets], dtype=torch.float) #One hot encoding.
        y = None if targets is None else torch.tensor(targets, dtype=torch.long)

        if all(x is not None for x in [featureMatrix, edge_index]):
            self.data = Data(x=featureMatrix, edge_index=edge_index, y=y)
        else:
            self.data = None
    
    def fromEmbedFetcher(self, embedFetched):
        """Automatically get torch_geometric accepted data format from the EmbedFetcher object.

        Args:
            embedFetched (EmbedFetcher): object
        """
        y = None if embedFetched.targets is None else torch.tensor(embedFetched.targets, dtype=torch.long)
        self.data = Data(x=embedFetched.featureMatrix, edge_index=embedFetched.edge_index, y=y)

    def showDataInfo(self):
        # Print information about the dataset
        print(f'\nNumber of nodes: {self.data.x.shape[0]}')
        print(f'Number of features: {self.data.num_features}')
        print(f'Has isolated nodes: {self.data.has_isolated_nodes()}')