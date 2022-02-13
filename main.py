
import serial
from time import sleep as sl
from random import randint as rand

# Size of the Matrix MxN
M = 8
N = 32

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


serialOrder = convertFromMatrixToString(leds_matrix_values)
mode = 2
if mode == 1:
    leds_matrix_values = getIncreaseDecreaseMatrix(leds_matrix_values)
else:
    leds_matrix_values = randomizeMatrix(leds_matrix_values)

bauds = 500000
port = 'COM3'
ser = serial.Serial(port, bauds)
sl(3)

# Minimum sleep time seems to be 0.08
sleepTime = 0.1

# Loop with a certain number of steps to write on the Serial and modify the matrix
nbSteps = 1000
for i in range(nbSteps):
    ser.write(serialOrder)
    leds_matrix_values = shiftMatrix(leds_matrix_values, False)
    serialOrder = convertFromMatrixToString(leds_matrix_values)
    sl(sleepTime)

# Closing the connection
ser.close()
