import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import os



def ConfusionMatrix(data, model, use_test_mask=False, saveFig=None, display=False):
    """Generates confusion matrix and classification report using sklearn. Displays classification report in terminal.

    Args:
        data (torch_geometric.data.Data): Should have targets.
        model (nn.Module): torch model
        use_test_mask (bool, optional): If True then takes only non-masked nodes for classification. Defaults to False.
        saveFig (str, optional): If "" saves into "Pictures" folder else to specified folder. Defaults to None - means no saving.
        display (bool, optional): If tkinter is installed then displays the confusion matrix. Generates error if tkinter not installed. Defaults to False.
    """
    if display:
        matplotlib.use("TkAgg")
    if use_test_mask:
        # only on masked nodes
        test_mask = ~data.train_mask

    y_pred = model(data.x, data.edge_index.T)
    y_pred = y_pred.argmax(dim=1)

    y_pred_test = (y_pred[test_mask]
                   if use_test_mask else y_pred).detach().numpy()
    y_test = (data.y[test_mask] if use_test_mask else data.y).detach().numpy()

    cm = confusion_matrix(y_true=y_test, y_pred=y_pred_test)

    dcm = ConfusionMatrixDisplay(
        confusion_matrix=cm, display_labels=['Non Fraud', 'Fraud'])

    dcm.plot(cmap='Purples')
    plt.title('Confusion Matrix')
    if display:
        plt.show()

    if saveFig is not None:
        picture_folder = saveFig
        name = "confusion_matrix.png"
        if saveFig=="":
            # Specify the path to the "Pictures" folder in home directory
            picture_folder = os.path.join(os.path.expanduser("~"), "Pictures")
        plt.savefig(os.path.join(picture_folder, name))
        print(f'Confusion matrix saved as "{name}" at {picture_folder}')

    print(classification_report(y_pred=y_pred_test, y_true=y_test))
