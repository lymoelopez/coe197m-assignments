import torch

class degree4AndLowerPolynomial(torch.nn.Module):

    def __init__(self, coefficients, degree):
        super().__init__()
        self.degree = degree
        self.a = torch.nn.Parameter(coefficients[0])
        
        if degree == 4:
            self.e = torch.nn.Parameter(coefficients[4])
        if degree <=4 and not degree == 2 and not degree == 1 and not degree == 0:
            self.d = torch.nn.Parameter(coefficients[3])
        if degree <= 4 and not degree == 1 and not degree == 0:
            self.c = torch.nn.Parameter(coefficients[2])
        if degree <= 4 and not degree == 0:
            self.b = torch.nn.Parameter(coefficients[1])

    def forward(self, x):
        if self.degree == 4:
            yPrediction = self.a + self.b * x + self.c * x ** 2 + self.d * x ** 3 + self.e * x **4
        elif self.degree == 3:
            yPrediction = self.a + self.b * x + self.c * x ** 2 + self.d * x ** 3 
        elif self.degree == 2:
            yPrediction = self.a + self.b * x + self.c * x ** 2 
        elif self.degree == 1:
            yPrediction = self.a + self.b * x 
        elif self.degree == 0:
            yPrediction = self.a

        return yPrediction

    def showPolynomial(self):
        if self.degree == 4:
            return f'y =  {self.e.item()} x^4 + {self.d.item()} x^3 + {self.c.item()} x^2 + {self.b.item()} x + {self.a.item()}'
        elif self.degree == 3:
            return f'y =  {self.d.item()} x^3 + {self.c.item()} x^2 + {self.b.item()} x + {self.a.item()}'
        elif self.degree == 2:
            return f'y =  {self.c.item()} x^2 + {self.b.item()} x + {self.a.item()}'
        elif self.degree == 1:
            return f'y =  {self.b.item()} x + {self.a.item()}' 

        return f'y =  {self.a.item()}'

    def save(self, modelPath='model/trainedModel.pth'):
        torch.save(self, modelPath)

