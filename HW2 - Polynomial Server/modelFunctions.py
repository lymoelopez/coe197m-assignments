import numpy as np
import pandas as pd
import torch
from torch.utils.data import TensorDataset, DataLoader
from RegscorePy import bic

def loadData(rawData):
    df = pd.read_csv(rawData)
    x = torch.Tensor(df['x'].values.astype(np.float32))
    y = torch.Tensor(df['y'].values.astype(np.float32))

    return x, y

def createMiniBatch(x, y, batchSize=1):
    dataset = TensorDataset(x, y)
    miniBatch = DataLoader(dataset, batch_size=batchSize, shuffle=True)

    return miniBatch

def findBestModel(degree1Model, degree2Model, degree3Model, degree4Model, x, y):
    modelList = [degree1Model, degree2Model, degree3Model, degree4Model]

    BICdegree1 = findBIC(degree1Model, x, y, 1)
    BICdegree2 = findBIC(degree2Model, x, y, 2)
    BICdegree3 = findBIC(degree3Model, x, y, 3)
    BICdegree4 = findBIC(degree4Model, x, y, 4)

    BIClist = [BICdegree1, BICdegree2, BICdegree3, BICdegree4]
    BICminimumIndex = min(range(len(BIClist)), key=BIClist.__getitem__)

    return modelList[BICminimumIndex]

def findBIC(model, x, yGroundTruth, polynomialDegree):
    # Bayesian Information Criterion (BIC)

    yPrediction = model(x).data.numpy().astype(float)
    yGroundTruth = yGroundTruth.numpy().astype(float)
    numberOfPredictiveVariables = polynomialDegree + 1

    BIC = bic.bic(yGroundTruth, yPrediction, numberOfPredictiveVariables)

    return BIC

