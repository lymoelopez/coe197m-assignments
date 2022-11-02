import cv2
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg) 
import tkinter as tk 
from tkinter import filedialog 

import os
import sys
import math 
from functools import partial



def findHomographyMatrix(sourcePoints, destinationPoints):

    # [knowns matrix][unknown homography matrix] = 0

    knownsMatrix = np.float32([])

    for i in range(4):

        X_sourcePoints = sourcePoints[i][0]
        Y_sourcepoints = sourcePoints[i][1]
        X_destinationPoints = destinationPoints[i][0]
        Y_destinationPoints = destinationPoints[i][1]

        a = -1 * X_destinationPoints * X_sourcePoints
        b = -1 * X_destinationPoints * Y_sourcepoints
    
        c = -1 * Y_destinationPoints * X_sourcePoints
        d = -1 * Y_destinationPoints * Y_sourcepoints

        firstRow = np.float32([X_sourcePoints, Y_sourcepoints, 1, 0, 0, 0, a, b, -X_destinationPoints])
        secondRow = np.float32([0, 0, 0, X_sourcePoints, Y_sourcepoints, 1, c, d, -Y_destinationPoints])

        knownsMatrix = np.append(knownsMatrix, firstRow)
        knownsMatrix = np.append(knownsMatrix, secondRow)

    knownsMatrix = np.reshape(knownsMatrix, (8,9))

    # Least Squares Estimation
    eigenValue, eigenVector = np.linalg.eig(np.matmul(knownsMatrix.T, knownsMatrix))
    eigenVector  = eigenVector[0:,np.argmin(eigenValue)]
    homography = np.reshape(eigenVector, (3,3))

    return homography 


def openFile():

    filePath = filedialog.askopenfilename() 

    return filePath  


def loadImage(filePath):

    rawImage = cv2.imread(filePath) 
    rawImage = cv2.cvtColor(rawImage,cv2.COLOR_BGR2RGB)

    return rawImage


def selectSourcePoints(rawImage):

    plt.figure("Select Source Points") 
    plt.imshow(rawImage)
    plt.title("Select points in a counterclockwise order [begin on the upper left corner]")
    plt.axis("off")
    rawInputPoints = plt.ginput(4)
    plt.close()

    return rawInputPoints


def createFigure(image, title): 

    fig, imagePlot = plt.subplots()
    imagePlot.imshow(image)
    imagePlot.set_title(title)
    imagePlot.axis("off")

    return fig, imagePlot


def plotSelectedSourcePoints(rawInputPoints, imagePlot): 

    x_rawInputPoints = [rawInputPoints[0][0], rawInputPoints[1][0], rawInputPoints[2][0], rawInputPoints[3][0], rawInputPoints[0][0]]
    y_rawInputPoints = [rawInputPoints[0][1], rawInputPoints[1][1], rawInputPoints[2][1], rawInputPoints[3][1], rawInputPoints[0][1]]

    imagePlot.plot(x_rawInputPoints, y_rawInputPoints, color='red', alpha=0.4, linewidth=2, solid_capstyle='round', zorder=2)


def plotFigure(fig):
 
    canvas = FigureCanvasTkAgg(fig, master = imageFrame)  
    canvas.get_tk_widget().pack(fill=tk.BOTH, side=tk.LEFT, expand= True)


def findSourcePoints(rawInputPoints):

    upperLeft = rawInputPoints[0]
    lowerLeft = rawInputPoints[1]
    lowerRight = rawInputPoints[2]
    upperRight = rawInputPoints[3]    

    sourcePoints = np.float32([upperLeft, lowerLeft, lowerRight, upperRight])

    return sourcePoints


def findDestinationPoints(sourcePoints): 

    #   A----D
    #   |    |
    #   B----C

    pointA = sourcePoints[0]
    pointB = sourcePoints[1]
    pointC = sourcePoints[2]
    pointD = sourcePoints[3]

    lineAD = np.linalg.norm([pointA[0] - pointD[0], pointA[1] - pointD[1]])
    lineBC = np.linalg.norm([pointB[0] - pointC[0], pointB[1] - pointC[1]])
    destinationWidth = max(int(lineAD), int(lineBC))

    lineAB = np.linalg.norm([pointA[0] - pointB[0], pointA[1] - pointB[1]])
    lineCD = np.linalg.norm([pointC[0] - pointD[0], pointC[1] - pointD[1]])
    destinationHeight = max(int(lineAB), int(lineCD))

    x_sourceCenter, y_sourceCenter = np.mean(sourcePoints, axis=0)

    halfDestinationWidth = int(destinationWidth/2)
    halfDestinationHeight = int(destinationHeight/2)

    # centered at (0, 0)
    destinationPoints = np.float32([
        [-halfDestinationWidth, -halfDestinationHeight],
        [-halfDestinationWidth, halfDestinationHeight],
        [halfDestinationWidth, halfDestinationHeight],
        [halfDestinationWidth, -halfDestinationHeight]
    ])

    return destinationPoints, destinationWidth, destinationHeight, x_sourceCenter, y_sourceCenter


def transformImage(rawImage, rawInputPoints, cropped):

    undistortSelectionButton.destroy()
    undistortFullButton.destroy()

    rawImageHeight, rawImageWidth = rawImage.shape[:2]
    undistortedImageWidth = undistortedImageHeight = round(math.hypot(rawImageHeight,rawImageWidth))

    sourcePoints = findSourcePoints(rawInputPoints)
    destinationPoints, destinationWidth, destinationHeight, x_sourceCenter, y_sourceCenter= findDestinationPoints(sourcePoints)

    if cropped:
        destinationPoints = destinationPoints + np.array([int(destinationWidth/2), int(destinationHeight/2)])
        undistortedImageWidth = destinationWidth
        undistortedImageHeight = destinationHeight
    else:
        x_destinationCenter = (x_sourceCenter/rawImageWidth) * undistortedImageWidth
        y_destinationCenter = (y_sourceCenter/rawImageHeight) * undistortedImageHeight
        destinationPoints = destinationPoints + np.array([x_destinationCenter, y_destinationCenter])

    homographyMatrix = findHomographyMatrix(sourcePoints, destinationPoints)

    undistortedImage = cv2.warpPerspective(rawImage, homographyMatrix, (undistortedImageWidth, undistortedImageHeight), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))

    return undistortedImage


def saveFile():
    filepath = filedialog.asksaveasfilename(defaultextension=".jpg")
    return filepath


def openButtonFunctions():

    filePath = openFile()
    if not filePath:
        return

    openButton.destroy()

    rawImage = loadImage(filePath)
    rawInputPoints = selectSourcePoints(rawImage)

    fig, imagePlot = createFigure(rawImage, 'Original Image')
    plotSelectedSourcePoints(rawInputPoints, imagePlot)
    plotFigure(fig)

    createUndistortButtons(rawImage, rawInputPoints)


def undistortButtonFunctions(rawImage, rawInputPoints, cropped):

    undistortedImage = transformImage(rawImage, rawInputPoints, cropped)
    fig, imagePlot = createFigure(undistortedImage, 'Undistorted Image')
    plotFigure(fig)

    createResetAndSaveButtons(undistortedImage)


def saveButtonFunction(undistortedImage, saveAs):

    if saveAs:
        filepath = saveFile()
        if not filepath:
            return
    else:
        filepath = "undistored.jpg"

    plt.imsave(filepath, undistortedImage)


def resetButtonFunction():
    python = sys.executable
    os.execl(python, python, * sys.argv)


def createUndistortButtons(rawImage, rawInputPoints):

    global undistortFullButton, undistortSelectionButton

    undistortFullButton = tk.Button(
        master = buttonFrame, 
        command = partial (undistortButtonFunctions, rawImage, rawInputPoints, 0),
        text = "Undistort (Full Image)"
    )

    undistortSelectionButton = tk.Button(
        master = buttonFrame, 
        command = partial (undistortButtonFunctions, rawImage, rawInputPoints, 1),
        text = "Undistort (Crop to Selection)"
    )

    undistortFullButton.pack(side=tk.LEFT)
    undistortSelectionButton.pack(side=tk.LEFT)


def createResetAndSaveButtons(undistortedImage):

    global resetButton, saveButton, saveAsButton

    resetButton = tk.Button(
        master = buttonFrame, 
        command = resetButtonFunction,
        text = "Try Again"
    )

    saveButton = tk.Button(
        master = buttonFrame, 
        command = partial (saveButtonFunction, undistortedImage, 0),
        text = "Save"
    )

    saveAsButton = tk.Button(
        master = buttonFrame, 
        command = partial (saveButtonFunction, undistortedImage, 1),
        text = "Save As"
    )

    resetButton.pack(side=tk.RIGHT)
    saveButton.pack(side=tk.LEFT)
    saveAsButton.pack(side=tk.LEFT)



window = tk.Tk()

window.title("Perspective Correction")
window.geometry("800x500")

buttonFrame = tk.Frame(master=window) 
buttonFrame.pack(fill=tk.BOTH)

imageFrame = tk.Frame(master=window)
imageFrame.pack(fill=tk.BOTH, expand= True)

openButton = tk.Button(
    master = buttonFrame, 
    command = openButtonFunctions,
    text = "Choose Image"
)

openButton.pack(side=tk.LEFT)

window.mainloop()