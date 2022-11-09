import cv2
from functools import partial
import math 
import numpy as np
import os
import sys
import matplotlib as mpl 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import filedialog 
import tkinter as tk 


def findHomographyMatrix(sourcePoints, destinationPoints):

    # [knowns matrix][unknown homography matrix] = 0
    knownsMatrix = np.float32([])

    for i in range(4):

        sourcePointsX = sourcePoints[i][0]
        sourcePointsY = sourcePoints[i][1]
        destinationPointsX = destinationPoints[i][0]
        destinationPointsY = destinationPoints[i][1]

        a = -destinationPointsX * sourcePointsX
        b = -destinationPointsX * sourcePointsY
        c = -destinationPointsY * sourcePointsX
        d = -destinationPointsY * sourcePointsY

        firstRow = np.float32([sourcePointsX, sourcePointsY, 1, 0, 0, 0, a, b, -destinationPointsX])
        secondRow = np.float32([0, 0, 0, sourcePointsX, sourcePointsY, 1, c, d, -destinationPointsY])

        knownsMatrix = np.append(knownsMatrix, firstRow)
        knownsMatrix = np.append(knownsMatrix, secondRow)

    knownsMatrix = np.reshape(knownsMatrix, (8, 9))

    # Least Squares Estimation
    eigenValue, eigenVector = np.linalg.eig(np.matmul(knownsMatrix.T, knownsMatrix))
    eigenVector  = eigenVector[0:, np.argmin(eigenValue)]
    homographyMatrix = np.reshape(eigenVector, (3, 3))

    return homographyMatrix 


def openFile():

    filePath = filedialog.askopenfilename() 

    return filePath  


def loadImage(filePath):

    rawImage = cv2.imread(filePath) 
    rawImage = cv2.cvtColor(rawImage, cv2.COLOR_BGR2RGB)

    return rawImage


def selectSourcePoints(rawImage):

    mpl.rcParams['toolbar'] = 'None' 
    plt.figure("Select Source Points") 
    plt.imshow(rawImage)
    plt.title("Select points in a counterclockwise order [begin on the upper left corner].")
    plt.axis("off")
    rawInputPoints = plt.ginput(4, 0)
    plt.close()

    return rawInputPoints


def createFigure(image, title): 

    fig, imagePlot = plt.subplots()
    imagePlot.imshow(image)
    imagePlot.set_title(title)
    imagePlot.axis("off")

    return fig, imagePlot


def plotSelectedSourcePoints(rawInputPoints, imagePlot): 

    rawInputPointsX = [rawInputPoints[0][0], rawInputPoints[1][0], rawInputPoints[2][0], rawInputPoints[3][0], rawInputPoints[0][0]]
    rawInputPointsY = [rawInputPoints[0][1], rawInputPoints[1][1], rawInputPoints[2][1], rawInputPoints[3][1], rawInputPoints[0][1]]

    imagePlot.plot(rawInputPointsX, rawInputPointsY, color='red', alpha=0.4, linewidth=2, solid_capstyle='round', zorder=2)


def plotFigure(fig):
    canvas = FigureCanvasTkAgg(fig, master=imageFrame)  
    canvas.get_tk_widget().pack(fill=tk.BOTH, side=tk.LEFT, expand= True)


def findSourcePoints(rawInputPoints):

    # sourcePoints = [upperLeft, lowerLeft, lowerRight, upperRight]
    sourcePoints = np.float32([rawInputPoints[0], rawInputPoints[1], rawInputPoints[2], rawInputPoints[3]])
    sourcePointsCenter = np.mean(sourcePoints, axis=0)

    return sourcePoints, sourcePointsCenter


def findCroppedDimensions(sourcePoints):

    pointA = sourcePoints[0]    #   A----D
    pointB = sourcePoints[1]    #   |    |
    pointC = sourcePoints[2]    #   B----C
    pointD = sourcePoints[3]

    lineAD = np.linalg.norm(pointA-pointD)
    lineBC = np.linalg.norm(pointB-pointC)
    lineAB = np.linalg.norm(pointA-pointB)
    lineCD = np.linalg.norm(pointC-pointD)

    croppedWidth = max(int(lineAD), int(lineBC))
    croppedHeight = max(int(lineAB), int(lineCD))
    croppedDimensions = [croppedWidth, croppedHeight]

    return croppedDimensions


def findDestinationPoints(croppedDimensions): 

    halfCroppedWidth = int(croppedDimensions[0]/2)
    halfCroppedHeight = int(croppedDimensions[1]/2)

    originCenteredDestinationPoints = np.float32([
        [-halfCroppedWidth, -halfCroppedHeight],
        [-halfCroppedWidth, halfCroppedHeight],
        [halfCroppedWidth, halfCroppedHeight],
        [halfCroppedWidth, -halfCroppedHeight]
    ])

    croppedDestinationCenter = np.array([halfCroppedWidth, halfCroppedHeight])
    croppedDestinationPoints = originCenteredDestinationPoints + croppedDestinationCenter

    return originCenteredDestinationPoints, croppedDestinationPoints 


def findRawImageDimensions(rawImage):

    rawImageHeight, rawImageWidth = rawImage.shape[:2]
    rawImageDiagonal = round(math.hypot(rawImageHeight, rawImageWidth))
    rawImageDimensions = [rawImageHeight, rawImageWidth, rawImageDiagonal]

    return rawImageDimensions 


def findFullDestinationCenter(sourcePointsCenter, rawImageDimensions): 

    rawImageHeight, rawImageWidth, rawImageDiagonal = rawImageDimensions

    destinationCenterX = (sourcePointsCenter[0]/rawImageWidth) * rawImageDiagonal
    destinationCenterY = (sourcePointsCenter[1]/rawImageHeight) * rawImageDiagonal
    fullDestinationCenter =  np.array([destinationCenterX, destinationCenterY])

    return fullDestinationCenter 


def findUndistortedImage(rawImage, rawInputPoints, cropped):

    sourcePoints, sourcePointsCenter = findSourcePoints(rawInputPoints)
    croppedDimensions = findCroppedDimensions(sourcePoints)
    originCenteredDestinationPoints, croppedDestinationPoints = findDestinationPoints(croppedDimensions)

    if cropped:
        destinationPoints = croppedDestinationPoints 
        undistortedImageWidth, undistortedImageHeight = croppedDimensions
    else:
        rawImageDimensions = findRawImageDimensions(rawImage)
        fullDestinationCenter  = findFullDestinationCenter(sourcePointsCenter, rawImageDimensions)
        destinationPoints = originCenteredDestinationPoints + fullDestinationCenter

        undistortedImageWidth = undistortedImageHeight = rawImageDimensions[2]
        
    homographyMatrix = findHomographyMatrix(sourcePoints, destinationPoints)    
    undistortedImage = cv2.warpPerspective(rawImage, homographyMatrix, (undistortedImageWidth, undistortedImageHeight), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

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

    undistortFullImageButton.destroy()
    undistortSelectionButton.destroy()

    undistortedImage = findUndistortedImage(rawImage, rawInputPoints, cropped)
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

    global undistortFullImageButton, undistortSelectionButton

    undistortFullImageButton = tk.Button(
        master = buttonFrame, 
        command = partial(undistortButtonFunctions, rawImage, rawInputPoints, 0),
        text = "Undistort (Full Image)"
    )

    undistortSelectionButton = tk.Button(
        master = buttonFrame, 
        command = partial(undistortButtonFunctions, rawImage, rawInputPoints, 1),
        text = "Undistort (Crop to Selection)"
    )

    undistortFullImageButton.pack(side=tk.LEFT)
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
        command = partial(saveButtonFunction, undistortedImage, 0),
        text = "Save"
    )

    saveAsButton = tk.Button(
        master = buttonFrame, 
        command = partial(saveButtonFunction, undistortedImage, 1),
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