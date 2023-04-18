import torch.nn as tnn
import torch_geometric.nn as tgnn

from collections import OrderedDict

class NNModel(tnn.Module):
    """A base neural network class which can handle layers of both torch and torch_geometric.
    The user needs to give modules as orderedDict. The class will handle creation of the network and forward method too.
    Extends: torch.nn.Module
    """
    def __init__(self, modules):
        """Sets the modules as self.layers.

        Args:
            modules (OrderedDict): Ordered dict of modules, can be of both torch and torch_geometric.
        """
        super(NNModel, self).__init__()
        self.layers = tnn.Sequential(modules)
    
    def forward(self, x, edge_index):
        h = x

        for layer in self.layers:
            h = (h, edge_index)
            if isinstance(layer, tgnn.conv.MessagePassing): #layers that needs (x,edge_index) as inputs
                h = layer(*h)
            else:  #layers that need only (x) as input
                h = layer(h[0])

        return h