
import serial
from time import sleep as sl
from random import randint as rand

ser = None
# Size of the Matrix MxN
M = 8
N = 32
# Minimum sleep time seems to be 0.008
DELAY_TIME = 0.01
NB_STEPS = 100
# Initialize the matrix values to 0
leds_matrix_values = [[0 for i in range(M)] for j in range(N)]


# Randomize the Matrix values
def randomizeMatrix(theMatrix):
    for i in range(len(theMatrix)):
        for j in range(len(theMatrix[i])):
            theMatrix[i][j] = rand(0, 1)
    return theMatrix


# Convert the matrix values to the String to send on Serial
def convertFromMatrixToString(theMatrix):
    finalString = b''
    for i in range(len(theMatrix)):
        stringLineValue = ''.join([str(value) for value in theMatrix[i]])
        intLineValue = int(stringLineValue, 2)
        byteLineValue = str.encode(str(intLineValue))
        finalString += byteLineValue + b';'
    return finalString[:-1] + b'>'


# Generate a specific matrix
def getIncreaseDecreaseMatrix(theMatrix):
    nb1 = 0
    vect = 1
    for i in range(len(theMatrix)):
        theMatrix[i] = [val for val in ('1'*nb1+'0'*(len(theMatrix[i])-nb1))]
        nb1 += vect
        if nb1 >= len(theMatrix[i]) or nb1 <= 0:
            vect *= -1
    return theMatrix


# Shifts all the values of the matrix in on or the other direction
def shiftMatrix(theMatrix, leftDirection=True):
    if leftDirection:
        return theMatrix[1:] + theMatrix[:1]
    else:
        return theMatrix[-1:] + theMatrix[0:-1]


def initConnection():
    global ser
    bauds = 500000
    port = 'COM3'
    ser = serial.Serial(port, bauds)
    sl(3)


# Closing the connection
def closeConnection():
    global ser
    ser.close()


def sendMatrix(theMatrix):
    global ser
    if ser is None:
        initConnection()
    ser.write(convertFromMatrixToString(theMatrix))


# Loop with a certain number of steps to write on the Serial and modify the matrix
def doCycle(t, nbSteps, theMatrix):
    for i in range(nbSteps):
        theMatrix = shiftMatrix(theMatrix, True)
        sendMatrix(theMatrix)
        sl(t)


def doStandardCycle():
    doCycle(DELAY_TIME, NB_STEPS, getIncreaseDecreaseMatrix(leds_matrix_values))


def doOtherCycle():
    doCycle(DELAY_TIME, NB_STEPS, randomizeMatrix(leds_matrix_values))


if __name__ == "__main__":
    initConnection()
    doCycle(DELAY_TIME, NB_STEPS, leds_matrix_values)
    closeConnection()