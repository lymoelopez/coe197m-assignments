import torch
from errorFunctions import printMAPE, printRSquared
from modelFunctions import loadData
from polynomialModel import degree4AndLowerPolynomial

def testModel(testData, modelPath):
    x, y = loadData(testData)
    model = torch.load(modelPath)
    yPrediction = model(x).data.numpy()

    print("")
    print("Testing Error")
    printMAPE(yPrediction, y.numpy())
    printRSquared(yPrediction.data, y)
    
