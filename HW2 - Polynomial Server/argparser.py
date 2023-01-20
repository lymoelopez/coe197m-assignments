import argparse

def argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--trainData', type=str, default=r'data/data_train.csv',help='select training data (default = data/data_train.csv)')
    parser.add_argument('--testData', type=str, default=r'data/data_test.csv',help='select testing data (default = data/data_test.csv)')
    parser.add_argument('--model', type=str, default='model/trainedModel.pth', help='select model for testing/select model save location and filename (default = model/trainedModel.pth)')

    parser.add_argument('--batchSize', type=int, default=1, help='select batch size (default = 1)')
    parser.add_argument('--lr', type=float, default=0.001, help='select learning rate (default = 0.001)')
    parser.add_argument('--epoch', type=int, default=200, help='nuber of training iterations (default = 200)')
    parser.add_argument('--degree', type=int, default=5, help='select model degree for training (default: use all to find best model)')

    parser.add_argument('--showTrainPlot', action='store_true', default=False, help='select to plot training data and polynomial model')
    parser.add_argument('--showTestPlot', action='store_true', default=False, help='select to plot testing data and polynomial model')

    parser.add_argument('--dontShowPolynomial', action='store_true', default=False, help='select to not print predicted polynomial')
    parser.add_argument('--dontTrainModel', action='store_true', default=False, help='select to not train model')
    parser.add_argument('--dontTestModel', action='store_true', default=False, help='select to not test model')

    return parser.parse_args()


