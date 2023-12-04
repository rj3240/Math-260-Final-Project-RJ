import numpy as np
import random
import math
import matplotlib.pyplot as plt
'''
x = testData[:,0]
y = testData[:,1]
plt.plot(x,y)
plt.show()
'''

def pathGenerator(oldPath): #Returns an np array of values that correspond to index locations of each coordinate point 
    n = len(oldPath)
    newPath = np.copy(oldPath)
    pivot1, pivot2 = np.random.choice(n, size=2, replace=False)
    newPath[[pivot1, pivot2]] = newPath[[pivot2, pivot1]]
    return newPath

def distanceCalc(path):
    n = len(path)
    distanceVector = np.zeros(n)

    for i in range(0,n-1):
        a = path[i,:]
        b = path[i+1,:]
        distanceVector[i] = np.linalg.norm(a-b) #Determining distance between two cities

    distanceVector[n-1] = np.linalg.norm(path[-1,:]-path[0,:]) #Filling in the return value to the start line
    distance = np.sum(distanceVector) #Calculating total distance
    return distance, distanceVector

def anneal(data, T, rate, iterations):
    bestDistancePerIter = []
    coordinates = np.copy(data)
    currentGuess = pathGenerator(coordinates)
    currentDistance,currentDistanceVec = distanceCalc(currentGuess)

    bestGuess = np.copy(currentGuess) #Determining a placeholder value for best guess
    bestDistance, bestDistanceVec = distanceCalc(bestGuess)
    
    #Using for loop to go through iterations specified in anneal function:
    for i in range(iterations):
        newGuess = pathGenerator(currentGuess)
        newDistance,newDistanceVec = distanceCalc(newGuess)
        if newDistance < currentDistance or random.random() < math.exp((currentDistance - newDistance)/T):
            currentGuess = newGuess
            currentDistance = newDistance
            if currentDistance < bestDistance:
                bestDistance = currentDistance
                bestDistanceVec = currentDistanceVec
        bestDistancePerIter.append(bestDistance)
        
        T = rate * T
        print(T)

    return bestGuess, bestDistance, bestDistancePerIter

def grapher(data,lineOpacity):
    x = data[:,0]
    y = data[:,1]
    plt.plot(x,y,alpha = lineOpacity)
    plt.scatter(x,y, marker = "o")
    plt.show()

if __name__ == "__main__":

    testData = np.array([[0,100],[100,0],[-100,0],[0,-100],[0,200],[200,0],[-200,0],[0,-200],[0,300],[300,0],[-300,0],[0,-300]])
    bestPath, distance,bestDistancePerRun = anneal(testData, 1000, 0.95, 100000)
    grapher(bestPath, 1)
    plt.plot(bestDistancePerRun)
    plt.show()


