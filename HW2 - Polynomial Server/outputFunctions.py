import torch
from matplotlib import pyplot as plt
from modelFunctions import loadData

def plotActualDataAndModel(x, y, yPrediction, rawDataLabel):
    plt.clf()
    plt.plot(x, y, 'go', label=rawDataLabel, alpha=0.5)
    plt.plot(x, yPrediction, '--', label='Polynomial Model', alpha=0.5)

    plt.legend(loc='best')
    plt.title("Polynomial Model vs. " + rawDataLabel)
    plt.show()

def printPolynomial(polynomialModel):
    print("")
    print("Your Polynomial is:")
    print(polynomialModel.showPolynomial())

def showPlot(rawData, modelPath, rawDataLabel):
    x, y = loadData(rawData)
    model = torch.load(modelPath)
    yPrediction = model(x).data.numpy()

    plotActualDataAndModel(x, y, yPrediction, rawDataLabel)