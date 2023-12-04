import numpy as np
import random
import math
import matplotlib.pyplot as plt

def readData(dataFile):
    dataFile = np.genfromtxt(dataFile, delimiter=",", dtype=None, names=True, encoding=None)
    coordinates = dataFile[['latitude', 'longitude']]
    print(coordinates)
    print(np.shape(coord))
    #nameData = dataFile[:,0:1]
    return coordinates

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
    plt.plot(x[0], y[0], marker = "+")
    plt.show()

if __name__ == "__main__":

    data = np.array([
    (32.377716, -86.300568),
    (58.301598, -134.420212),
    (33.448143, -112.096962),
    (34.746613, -92.288986),
    (38.576668, -121.493629),
    (39.739227, -104.984856),
    (41.764046, -72.682198),
    (39.157307, -75.519722),
    (21.307442, -157.857376),
    (30.438118, -84.281296),
    (33.749027, -84.388229),
    (43.617775, -116.199722),
    (39.798363, -89.654961),
    (39.768623, -86.162643),
    (41.591087, -93.603729),
    (39.048191, -95.677956),
    (38.186722, -84.875374),
    (30.457069, -91.187393),
    (44.307167, -69.781693),
    (38.978764, -76.490936),
    (42.358162, -71.063698),
    (42.733635, -84.555328),
    (44.955097, -93.102211),
    (32.303848, -90.182106),
    (38.579201, -92.172935),
    (46.585709, -112.018417),
    (40.808075, -96.699654),
    (39.163914, -119.766121),
    (43.206898, -71.537994),
    (40.220596, -74.769913),
    (35.68224, -105.939728),
    (35.78043, -78.639099),
    (46.82085, -100.783318),
    (42.652843, -73.757874),
    (39.961346, -82.999069),
    (35.492207, -97.503342),
    (44.938461, -123.030403),
    (40.264378, -76.883598),
    (41.830914, -71.414963),
    (34.000343, -81.033211),
    (44.367031, -100.346405),
    (36.16581, -86.784241),
    (30.27467, -97.740349),
    (40.777477, -111.888237),
    (44.262436, -72.580536),
    (37.538857, -77.43364),
    (47.035805, -122.905014),
    (38.336246, -81.612328),
    (43.074684, -89.384445),
    (41.140259, -104.820236)
]
)
    print(data)

    #coordinates = readData("us-state-capitals.csv")
    #testData = np.array([[0,100],[100,0],[-100,0],[0,-100],[0,200],[200,0],[-200,0],[0,-200],[0,300],[300,0],[-300,0],[0,-300]])
    #random_matrix = np.random.rand(2000, 2)
    bestPath, distance,bestDistancePerRun = anneal(data, 10000, 0.95, 10000)

    grapher(bestPath, 1)
    
    plt.plot(bestDistancePerRun)
    plt.show()


