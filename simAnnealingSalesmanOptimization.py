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

def latLongCalc(coord1,coord2): #coordinate is a (,2) dimension np array. Everything is in miles
    delta = coord2 - coord1
    deltLatit = delta[0] * 69 #conversion to miles
    deltLong = delta[1] * 54.6 #conversion to miles
    deltaMiles = np.sqrt(deltLatit ** 2 + deltLong ** 2)
    return deltaMiles

def distanceCalc(path):
    n = len(path)
    distanceVector = np.zeros(n)

    for i in range(0,n-1):
        a = path[i,:]
        b = path[i+1,:]
        distanceVector[i] = latLongCalc(a,b)

    distanceVector[n-1] = latLongCalc(path[-1,:],path[0,:]) #Filling in the return value to the start line
    distance = np.sum(distanceVector) #Calculating total distance
    return distance, distanceVector

def timeCostCalc(data,airCriteria,airSpeed,airCost,carSpeed,carCost, selector):
    n = len(data)
    _,distances = distanceCalc(data)
    timeVector = np.zeros(n)
    costVector = np.zeros(n)
    for i in range(0,n-1):
        if distances[i] > airCriteria:
            timeVector[i] = distances[i]/airSpeed
            costVector[i] = distances[i] * airCost
        else:
            timeVector[i] = distances[i]/carSpeed
            costVector[i] = distances[i] * carCost
    time = np.sum(timeVector)
    cost = np.sum(costVector)

    if selector == "time":
        return time,timeVector
    elif selector == "cost":
        return cost,costVector

def annealDistance(data, T, rate, iterations):

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

def annealTime(data, T, rate, iterations,airSpeed,airCriteria,airCost,carSpeed,carCost):

    bestTimePerIter = []
    coordinates = np.copy(data)
    currentGuess = pathGenerator(coordinates)
    currentTime,currentTimeVec = timeCostCalc(currentGuess,airCriteria,airSpeed,airCost,carSpeed,carCost, "time")

    bestGuess = np.copy(currentGuess) #Determining a placeholder value for best guess
    bestTime, bestTimeVec = timeCostCalc(bestGuess,airCriteria,airSpeed,airCost,carSpeed,carCost, "time")
    
    #Using for loop to go through iterations specified in anneal function:
    for i in range(iterations):
        newGuess = pathGenerator(currentGuess)
        newTime,newTimeVec = timeCostCalc(newGuess,airCriteria,airSpeed,airCost,carSpeed,carCost, "time")
        if newTime < currentTime or random.random() < math.exp((currentTime - newTime)/T):
            currentGuess = newGuess
            currentTime = newTime
            if newTime < bestTime:
                bestTime = currentTime
                bestTimeVec = currentTimeVec
        bestTimePerIter.append(bestTime)
        
        T = rate * T
        print(T)

    return bestGuess, bestTime, bestTimePerIter

def annealCost(data, T, rate, iterations,airSpeed,airCriteria,airCost,carSpeed,carCost):

    bestCostPerIter = []
    coordinates = np.copy(data)
    currentGuess = pathGenerator(coordinates)
    currentCost,currentCostVec = timeCostCalc(currentGuess,airCriteria,airSpeed,airCost,carSpeed,carCost, "cost")

    bestGuess = np.copy(currentGuess) #Determining a placeholder value for best guess
    bestCost, bestCostVec = timeCostCalc(bestGuess,airCriteria,airSpeed,airCost,carSpeed,carCost, "cost")
    
    #Using for loop to go through iterations specified in anneal function:
    for i in range(iterations):
        newGuess = pathGenerator(currentGuess)
        newCost,newCostVec = timeCostCalc(newGuess,airCriteria,airSpeed,airCost,carSpeed,carCost, "cost")
        if newCost < currentCost or random.random() < math.exp((currentCost - newCost)/T):
            currentGuess = newGuess
            currentCost = newCost
            if newCost < bestCost:
                bestCost = currentCost
                bestCostVec = currentCostVec
        bestCostPerIter.append(bestCost)
        
        T = rate * T
        print(T)

    return bestGuess, bestCost, bestCostPerIter

def annealOptimization(data, T, rate, iterations,airSpeed,airCriteria,airCost,carSpeed,carCost, optimizationType):
    if optimizationType == "distance":
        return annealDistance(data, T, rate, iterations)
    elif optimizationType == "cost":
        return annealCost(data, T, rate, iterations,airSpeed,airCriteria,airCost,carSpeed,carCost)
    elif optimizationType == "time":
        return annealTime(data, T, rate, iterations,airSpeed,airCriteria,airCost,carSpeed,carCost)

def pathGrapher(data, lineColor):
    x = data[:,0]
    y = data[:,1]
    plt.plot(x,y,alpha = 1,color=lineColor)
    plt.scatter(x,y, marker = "o", color="black", alpha = 1)
    plt.plot(x[0], y[0], marker = "o", markersize = 10, color="orange")
    plt.xlabel("Latitude (deg.)")
    plt.ylabel("Longitude (deg.)")
    plt.title("Optimal Distance Path")

    # Plot arrows
    plt.show()

if __name__ == "__main__":

    T = 100000
    rate = 0.995
    iterations = 10000

    #######################################################################################
    #SCENARIO 1: Traveling Salesman Cities: Distance Optimization #########################
    #######################################################################################

    airSpeed1 = 600 #mph
    airCriteria1 = 300 #maximum of 4 hour drive
    airCost1 = 10.0 #dollars
    carSpeed1 = 60 #mph
    carCost1 = 1 #dollars
    
    
    data1 = np.array([
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
    (41.140259, -104.820236)])
    
    #######################################################################################

    ##########################################
    #SCENARIO 2: Traveling In Circle:
    ##########################################

    airSpeed2 = 500 #mph
    airCriteria2 = 300 #maximum of 4 hour drive
    airCost2 = 1 #dollars
    carSpeed2 = 70 #mph
    carCost2 = 3.0 #dollars

    radius = 1000
    points = 15
    theta = np.linspace(0, 2 * np.pi, points)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    # Create the n by 2 array of points
    data2 = np.array([x, y]).T

    #######################################################################################

    scenario1 = True
    scenario2 = False
    if scenario1:

        bestPath, distance,bestDistancePerRun = annealOptimization(data1,T,rate,iterations,airSpeed1, airCriteria1, airCost1, carSpeed1, carCost1, "distance")
        bestTimePath, bestTime, bestTimePerIter = annealOptimization(data1,T,rate,iterations,airSpeed1, airCriteria1, airCost1, carSpeed1, carCost1, "time")
        bestCostPath, bestCost, bestCostPerIter = annealOptimization(data1,T,rate,iterations,airSpeed1, airCriteria1, airCost1, carSpeed1, carCost1, "cost")
        print(bestTime)
        print(bestCost)

        pathGrapher(bestPath, "red")
        pathGrapher(bestTimePath, "green")
        pathGrapher(bestCostPath, "blue")
        #plt.show()

        plt.plot(bestTimePerIter)
        plt.xlabel("Iteration Count")
        plt.ylabel("Total Time (Hr)")
        plt.title("Simulated Annealing Time Performance over Iteration")
        plt.show()

        plt.plot(bestCostPerIter)
        plt.xlabel("Iteration Count")
        plt.ylabel("Total Cost (USD)")
        plt.title("Simulated Annealing Cost Performance over Iteration")
        plt.show()
    
    elif scenario2:

        bestPath, distance,bestDistancePerRun = annealDistance(data2, 100000, 0.995, 10000)
        bestTimePath, bestTime, bestTimePerIter = annealTime(data2, 100000,0.995, 10000, airSpeed2, airCriteria2, airCost2, carSpeed2, carCost2)
        bestCostPath, bestCost, bestCostPerIter = annealCost(data2, 100000,0.995, 10000, airSpeed2, airCriteria2, airCost2, carSpeed2, carCost2)
        print(bestTime)
        print(bestCost)

        pathGrapher(bestPath, "red")
        pathGrapher(bestTimePath, "green")
        pathGrapher(bestCostPath, "blue")
        plt.show()

        plt.plot(bestTimePerIter)
        plt.xlabel("Iteration Count")
        plt.ylabel("Total Time (Hr)")
        plt.title("Simulated Annealing Time Performance over Iteration")
        plt.show()

        plt.plot(bestCostPerIter)
        plt.xlabel("Iteration Count")
        plt.ylabel("Total Cost (USD)")
        plt.title("Simulated Annealing Cost Performance over Iteration")
        plt.show()



