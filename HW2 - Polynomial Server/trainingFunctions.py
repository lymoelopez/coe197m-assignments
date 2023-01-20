from polynomialModel import degree4AndLowerPolynomial
import tinygrad.nn.optim as optim
import torch
import math

def learningRateScheduler(epoch, optimizer, scheduler, isTinyGrad):
    if isTinyGrad:
        optimizer.lr = scheduler * (0.95 ** (epoch))
    else:
        scheduler.step()

def findSGD(model, epoch, dataloader, optimizer, criterion, scheduler, isTinyGrad=0):
    for i in range(epoch):
        for id_batch, (x_batch, y_batch) in enumerate(dataloader):
            optimizer.zero_grad()
            y_batch_pred = model(x_batch)
            loss = criterion(y_batch_pred, y_batch)
            loss.backward()
            optimizer.step()

        learningRateScheduler(epoch, optimizer, scheduler, isTinyGrad)

    return model


def optimizeModel(model, dataloader, learningRate, epoch):
    
    criterion = torch.nn.SmoothL1Loss()

    print("still training .")
    torchLearningRate = learningRate/(10**4)
    torchEpoch = math.floor(epoch * 0.3)
    torchOptimizer = torch.optim.SGD(model.parameters(), lr=torchLearningRate, momentum=0.95) 
    scheduler = torch.optim.lr_scheduler.ExponentialLR(torchOptimizer, gamma=0.95)

    findSGD(model, torchEpoch, dataloader, torchOptimizer, criterion,scheduler)

    print("still training . .")
    tinyGradLearningRate = learningRate
    tinyGradEpoch = epoch
    tinyGradOptimizer = optim.SGD(model.parameters(), lr=tinyGradLearningRate) 
    lr0 = tinyGradOptimizer.lr

    findSGD(model, tinyGradEpoch, dataloader, tinyGradOptimizer, criterion, lr0, True)


def createAndOptimizeModel(initialCoefficients, modelDegree, dataloader, learningRate, epoch):
    polynomialModel = degree4AndLowerPolynomial(coefficients=initialCoefficients, degree=modelDegree)
    optimizeModel(polynomialModel, dataloader, learningRate, epoch)

    return polynomialModel