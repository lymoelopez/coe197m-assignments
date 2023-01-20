import numpy as np
import sklearn.metrics as metrics

def findMAPE(prediction, groundTruth):
    MAE = (np.abs((prediction - groundTruth)/groundTruth)).mean()
    MAPE = MAE * 100
    return MAPE

def printMAPE(prediction, groundTruth):
    MAPE = findMAPE(prediction, groundTruth)
    print("Mean Absolute Percentage Error:", "%.2f" % MAPE + "%")

def printRSquared(prediction, groundTruth):
    RSquared = metrics.r2_score(groundTruth, prediction)
    RSquared = RSquared * 100
    print("R-Squared (r2 Score):", "%.2f" % RSquared + "%")
