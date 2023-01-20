# Polynomial Solver

A python program used to estimate the degree and coefficients of a degree 4 or lower polynomial. This solver implments SGD with  [tinygrad](https://github.com/geohot/tinygrad).


## Usage

``` bash
python3 solver.py [-h] [--trainData TRAINDATA] [--testData TESTDATA] [--model MODEL] [--batchSize BATCHSIZE] [--lr LR] [--epoch EPOCH] [--degree DEGREE]
                 [--showTrainPlot] [--showTestPlot] [--dontShowPolynomial] [--dontTrainModel] [--dontTestModel]
```
## Optional Arguments
* `-h, --help`= show this help message and exit
* `--trainData TRAINDATA` = select training data (default: data/data_train.csv)
* `--testData TESTDATA` = select testing data (default: data/data_test.csv)
* `--model MODEL` = select model for testing/select model save location and filename (default: model/trainedModel.pth)
* `--batchSize BATCHSIZE` = select batch size (default: 1)
* `--lr LR` = select learning rate (default: 0.001)
* `--epoch EPOCH` = nuber of training iterations (default: 150)
* `--degree DEGREE` = select model degree for training (default: find best model)
* `--showTrainPlot` = select to plot training data and polynomial model
* `--showTestPlot` = select to plot testing data and polynomial model
* `--dontShowPolynomial` = select to not print predicted polynomial
* `--dontTrainModel` = select to not train model
* `--dontTestModel` = select to not test model


## References

[1] [Polynomial regression with PyTorch](https://soham.dev/posts/polynomial-regression-pytorch/)

[3] [Linear regression](https://github.com/madsendennis/notebooks/blob/master/pytorch/1_Linear_regression.ipynb)

[3] [PYTORCH: CUSTOM NN MODULES](https://pytorch.org/tutorials/beginner/examples_nn/polynomial_module.html)


[4] [Creating a PyTorch model to fit a polynomial distribution](https://discuss.pytorch.org/t/creating-a-pytorch-model-to-fit-a-polynomial-distribution/161595)


[5] [Pytorch and Polynomial Linear Regression issue](https://stackoverflow.com/questions/42795226/pytorch-and-polynomial-linear-regression-issue)


[6] [How to include batch size in pytorch basic example?](https://stackoverflow.com/questions/51735001/how-to-include-batch-size-in-pytorch-basic-example)


[7] [RegscorePy 1.1](https://pypi.org/project/RegscorePy/)

[8] [How to realize a polynomial regression in Pytorch / Python](https://stackoverflow.com/questions/55920015/how-to-realize-a-polynomial-regression-in-pytorch-python)

[9] [Learning Rate Schedules and Adaptive Learning Rate Methods for Deep Learning](https://towardsdatascience.com/learning-rate-schedules-and-adaptive-learning-rate-methods-for-deep-learning-2c8f433990d1)
