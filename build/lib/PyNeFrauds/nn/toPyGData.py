import torch
from torch_geometric.data import Data
import numpy as np
import random

class PyGDataWrapper():
    def __init__(self, featureMatrix=None, edge_index=None, targets=None ):
        """Class that wraps the torch_geometric.data.Data for this library.
        Aim is to make handling, manipulating torch_geometric accepted data easy.
        Stores torch_geometric.data.Data in self.data
        Args: [Can be of type numpy.ndarray or python number list, transforms and stores them as torch.tensor()]
            featureMatrix (optional): Defaults to None.
            edge_index (optional): Defaults to None.
            targets (optional): Defaults to None.
        """
        featureMatrix = None if featureMatrix is None else torch.tensor(featureMatrix, dtype=torch.float)
        edge_index = None if edge_index is None else torch.tensor(edge_index, dtype=torch.long)
        # ty = torch.tensor([[1,0] if x==0 else [0,1] for x in targets], dtype=torch.float) #One hot encoding.
        y = None if targets is None else torch.tensor(targets, dtype=torch.long)

        if all(x is not None for x in [featureMatrix, edge_index]):
            self.data = Data(x=featureMatrix, edge_index=edge_index, y=y)
        else:
            self.data = None
    
    def from_embed_fetcher(self, embedFetched, frac=0):
        """Automatically get torch_geometric accepted data format from the EmbedFetcher object.

        Args:
            embedFetched (EmbedFetcher): object
        """
        x = torch.tensor(embedFetched.featureMatrix, dtype=torch.float)
        edge_index = torch.tensor(embedFetched.edge_index, dtype=torch.long)
        y = None if embedFetched.targets is None else torch.tensor(embedFetched.targets, dtype=torch.long)
        self.data = Data(x=x, edge_index=edge_index, y=y)
        self.set_train_mask(frac=frac)

    def set_train_mask(self, frac):
        n_nodes = self.data.x.shape[0]
        n_mask = int(frac * n_nodes) #no of nodes to be not used for training
        train_mask = torch.tensor(np.array([True]*n_nodes))

        mask_indexes = random.sample(list(range(0,n_nodes)), n_mask)
        train_mask[mask_indexes] = False
        self.data.train_mask = train_mask

    def show_data_info(self):
        # Print information about the dataset
        print(f'\nNumber of nodes: {self.data.x.shape[0]}')
        print(f'Number of features: {self.data.num_features}')
        print(f'Has isolated nodes: {self.data.has_isolated_nodes()}')