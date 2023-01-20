import torch
from argparser import argparser
from trainModel import trainModel
from outputFunctions import printPolynomial, showPlot
from testModel import testModel

def train(args):
    trainData = args.trainData
    modelPath = args.model
    batchSize = args.batchSize
    epoch = args.epoch
    learningRate = args.lr
    degree = args.degree

    trainModel(trainData, batchSize, learningRate, epoch, modelPath, degree)

def test(args):
    testData = args.testData
    modelPath = args.model

    testModel(testData, modelPath)

def main(args):

    trainModel = not args.dontTrainModel
    showTrainPlot =  args.showTrainPlot
    testModel = not args.dontTestModel
    showTestPlot = args.showTestPlot
    showPolynomial = not args.dontShowPolynomial

    if trainModel:
        train(args)

    if testModel:
        test(args)

    if showTrainPlot:
        rawData = args.trainData
        modelPath =  args.model
        rawDataLabel = "Training Data"

        showPlot(rawData, modelPath, rawDataLabel)

    if showTestPlot:
        rawData = args.testData
        modelPath =  args.model
        rawDataLabel = "Testing Data"

        showPlot(rawData, modelPath, rawDataLabel)
    
    if showPolynomial:
        modelPath = args.model
        polynomialModel = torch.load(modelPath)

        printPolynomial(polynomialModel)

if __name__ == '__main__':
    args = argparser()
    main(args)

