import torch
from .ModelBuilder import NNModel

def train(model, data, criterion=None, optimizer=None, n_epoch=20, quiet=False, print_interval=1):

    criterion = torch.nn.CrossEntropyLoss() if criterion is None else criterion
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01) if optimizer is None else optimizer

    losses = []
    accuracies = []

    for epoch in range(n_epoch):
        optimizer.zero_grad()
        y_pred = model(data.x, data.edge_index.T)
        loss = criterion(y_pred, data.y)
        # acc = accuracy(y_pred.argmax(dim=1), data.y)
        loss.backward()
        optimizer.step()

        losses.append(loss.item())
        # accuracies.append(acc)

        if not quiet and epoch % (print_interval) == 0:
            print(
                f'epoch: {epoch}/{n_epoch} \t loss:{loss:.3f}') # \t f1-score:{acc*100:.3f}')

    return model, losses #, accuracies
