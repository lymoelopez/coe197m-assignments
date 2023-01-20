import torch
from modelFunctions import createMiniBatch, loadData, findBestModel
from trainingFunctions import createAndOptimizeModel

def trainModel(trainData, batchSize, learningRate, epoch, modelPath, degree):
    x, y = loadData(trainData)
    miniBatch = createMiniBatch(x, y, batchSize)
    initialCoefficients = torch.randn(5).requires_grad_()

    if degree >= 5 or degree == 1:
        print("Training a First Degree Model . . .")
        degree1Model = createAndOptimizeModel(initialCoefficients, 1, miniBatch, learningRate, epoch)
        bestModel = degree1Model
    if degree >= 5 or degree == 2:
        print("Training a Second Degree Model . . .")
        degree2Model = createAndOptimizeModel(initialCoefficients, 2, miniBatch, learningRate, epoch)
        bestModel = degree2Model
    if degree >= 5 or degree == 3:    
        print("Training a Third Degree Model . . .")
        degree3Model = createAndOptimizeModel(initialCoefficients, 3, miniBatch, learningRate, epoch)
        bestModel = degree3Model
    if degree >= 5 or degree == 4:
        print("Training a Fourth Degree Model . . .")
        degree4Model = createAndOptimizeModel(initialCoefficients, 4, miniBatch, learningRate, epoch)
        bestModel = degree4Model

    if degree >= 5:
        print("Selecting the Best Model . . .")
        bestModel = findBestModel(degree1Model, degree2Model, degree3Model, degree4Model, x, y)
        
    bestModel.save(modelPath)




