import numpy as np
import random
import math
import matplotlib.pyplot as plt

testData = np.array([[0,100],[100,0],[-100,0],[0,-100]])
x = testData[:,0]
y = testData[:,1]
#plt.scatter(x,y)
#plt.show()

def pathGenerator(dataInput):
    
    path = np.copy(dataInput)
    n = len(path)

    pivot1 = random.randint(0,n-1)
    secondPivotSelect = False
    
    while secondPivotSelect == False:
        pivot2 = random.randint(0,n-1)
        if pivot2 != pivot1:
            secondPivotSelect = True

    path[pivot1,:], path[pivot2,:] = path[pivot2,:], path[pivot1,:]

    return path

def distanceCalc(path):

    n = len(path)
    distanceVector = np.zeros(n)

    for i in range(0,n-1):
        a = path[i,:]
        b = path[i+1,:]
        distanceVector[i] = np.linalg.norm(a-b) #Determining distance between two cities

    distanceVector[n-1] = np.linalg.norm(path[-1,:]-path[0,:]) #Filling in the return value to the start line
    distance = np.linalg.norm(distanceVector)
    return distance, distanceVector

def acceptanceProb(init,new,temp):

    if new > init:
        acceptanceProb = 1
    else:
        acceptanceProb = math.exp((new-init)/temp)
    return acceptanceProb 

def simAnneal():
    print("hello")
    return simAnneal

