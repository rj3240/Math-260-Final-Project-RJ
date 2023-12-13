import numpy as np
import random
import math
import matplotlib.pyplot as plt

"""
pathGenerator is used to create a new path between coordinate points from an older path.
A new path is generated by swapping two elements of the older path, and then calculating the distance between coordinates
of the new path.

INPUT
oldPath:  the previous path, which is a n by 2 numpy array

OUTPUT
newPath: the new path, which is a n by 2 numpy array that has two elements swapped
"""

def pathGenerator(oldPath): #Returns an np array of values that correspond to index locations of each coordinate point 
    n = len(oldPath)
    newPath = np.copy(oldPath)
    pivot1, pivot2 = np.random.choice(n, size=2, replace=False) #Choosing two unique pivots
    newPath[[pivot1, pivot2]] = newPath[[pivot2, pivot1]] #Creating a new path by swapping the two previously generated pivots
    return newPath

"""
LatLongCalc is used to easily convert from latitude and longitude degrees of measure to miles.
This is necessary as otherwise distance measurements would have to be appropriately scaled for the degree scale.

INPUTS
coord1: first coordinate point
coord2: second coordinate point (immediate point after coord1 in path)

OUTPUT
deltaMiles: the distance between the two coordinate points, outputted in miles.
"""

def latLongCalc(coord1,coord2): #coordinate is a (,2) dimension np array. Everything is in miles
    delta = coord2 - coord1
    deltLatit = delta[0] * 69 #conversion to miles
    deltLong = delta[1] * 54.6 #conversion to miles
    deltaMiles = np.sqrt(deltLatit ** 2 + deltLong ** 2)
    return deltaMiles

"""
pathGenerator is used to create a new path between coordinate points from an older path.
A new path is generated by swapping two elements of the older path, and then calculating the distance between coordinates
of the new path.

INPUT
path: the path through which the salesman travels, which is a n by 2 numpy array

OUTPUTS
distance: the total distance traveled, including the distance from the end point to the starting point
distanceVector: vector corresponding to the distances between points along the path.
"""

def distanceCalc(path):
    n = len(path)
    distanceVector = np.zeros(n)
    #Calculating the difference between 
    for i in range(0,n-1):
        a = path[i,:]
        b = path[i+1,:]
        distanceVector[i] = latLongCalc(a,b) #Converting from coordinates to distances

    distanceVector[n-1] = latLongCalc(path[-1,:],path[0,:]) #Filling in the return value to the start line
    distance = np.sum(distanceVector) #Calculating total distance
    return distance, distanceVector

"""
timeCostCalc is used to calculate the total time or cost required to traverse a certain path. 
Multiple parameters are input to determine characteristics of air or land travel.

INPUTS
data: the path through which the salesman travels, which is a n by 2 numpy array
airCriteria: maximum distance in miles salesman is willing to drive
airSpeed: average speed of air travel, measured in mph
airCost: cost of air travel, measured in dollars per hour
carSpeed: average speed of car travel, measured in mph
carCost: cost of car travel, measured in dollars per hour
selector: used to switch between which values are returned by timeCostCalc
"time" returns time related information
"cost" returns cost related information

OUTPUTS
time: the total time elapsed over path
timeVector: vector corresponding to the time elapsed between points along the path.
cost: the total cost elapsed over path
costVector: vector corresponding to the cost elapsed between points along the path.
"""

def timeCostCalc(data,airCriteria,airSpeed,airCost,carSpeed,carCost, selector):
    n = len(data)
    _,distances = distanceCalc(data)
    timeVector = np.zeros(n+1)
    costVector = np.zeros(n+1)
    #Using for loop to go through each distance of the distance vector:
    for i in range(0,n):
        if distances[i] > airCriteria: #Air criteria is given as a distance in miles, corresponding to maximum distance salesmen would want to drive.
            timeVector[i] = distances[i]/airSpeed 
            costVector[i] = distances[i] * airCost
        else: #Corresponds to salesman choosing to drive
            timeVector[i] = distances[i]/carSpeed
            costVector[i] = distances[i] * carCost
    time = np.sum(timeVector) #Calculating the total time required to traverse path by summing up individual time intervals
    cost = np.sum(costVector) #Calculating the total cost required to traverse path by summing up individual cost intervals

    #Selector is used to determine whether time or cost conversions will be returned
    if selector == "time":
        return time,timeVector
    elif selector == "cost":
        return cost,costVector
    else: #Returning a value error if incorrect selector is chosen
        return ValueError

"""
annealDistance is used to minimize the total distance traveled with the Simulated Annealing method. 
Multiple parameters are input to determine characteristics of air or land travel.

INPUTS
data: the path through which the salesman travels, which is a n by 2 numpy array
T: starting temperature of Simulated Annealing temperature function (exponential decay model)
rate: rate of temperature decay
iterations: number of iterations ran by simulated annealing optimization

OUTPUTS
bestGuess: the path which best minimizes distance
bestDistance: the best distance after all iterations
bestDistancePerIter: the best distance stored per single iteration
"""

def annealDistance(data, T, rate, iterations):

    bestDistancePerIter = []
    coordinates = np.copy(data)
    currentGuess = pathGenerator(coordinates) #Creating a first path guess.
    currentDistance,currentDistanceVec = distanceCalc(currentGuess) 
    #Determining the total distance and associated distance vector of the initial guess

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
                bestDistanceVec = currentDistanceVec #Updating best guess if current guess is more optimal (least distance)
        bestDistancePerIter.append(bestDistance) #Storing the best guess per iteration
        
        T = rate * T #Temperature decreases according to exponential rate
    return bestGuess, bestDistance, bestDistancePerIter

"""
annealTime is used to minimize the total time traveled with the Simulated Annealing method. 
Multiple parameters are input to determine characteristics of air or land travel.

INPUTS
data: the path through which the salesman travels, which is a n by 2 numpy array
T: starting temperature of Simulated Annealing temperature function (exponential decay model)
rate: rate of temperature decay
iterations: number of iterations ran by simulated annealing optimization
airCriteria: maximum distance in miles salesman is willing to drive
airSpeed: average speed of air travel, measured in mph
airCost: cost of air travel, measured in dollars per hour
carSpeed: average speed of car travel, measured in mph
carCost: cost of car travel, measured in dollars per hour

OUTPUTS
bestGuess: the path which best minimizes time elapsed
bestTime: the best elapsed time after all iterations
bestTimePerIter: the best elapsed time stored per single iteration
"""

def annealTime(data, T, rate, iterations,airSpeed,airCriteria,airCost,carSpeed,carCost):

    bestTimePerIter = []
    coordinates = np.copy(data)
    currentGuess = pathGenerator(coordinates)
    currentTime,currentTimeVec = timeCostCalc(currentGuess,airCriteria,airSpeed,airCost,carSpeed,carCost, "time")
    #Determining the total distance and associated distance vector of the initial guess

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
                bestTimeVec = currentTimeVec #Updating best guess if current guess is more optimal (less time expensive)
        bestTimePerIter.append(bestTime) #Updating best guess if current guess is more optimal (less expensive)
        
        T = rate * T #Temperature decreases according to exponential rate
    return bestGuess, bestTime, bestTimePerIter

"""
annealCost is used to minimize the total cost incurred with the Simulated Annealing method. 
Multiple parameters are input to determine characteristics of air or land travel.

INPUTS
data: the path through which the salesman travels, which is a n by 2 numpy array
T: starting temperature of Simulated Annealing temperature function (exponential decay model)
rate: rate of temperature decay
iterations: number of iterations ran by simulated annealing optimization
airCriteria: maximum distance in miles salesman is willing to drive
airSpeed: average speed of air travel, measured in mph
airCost: cost of air travel, measured in dollars per hour
carSpeed: average speed of car travel, measured in mph
carCost: cost of car travel, measured in dollars per hour

OUTPUTS
bestGuess: the path which best minimizes cost
bestCost: the best incurred cost after all iterations
bestCostPerIter: the best incurred cost stored per single iteration
"""

def annealCost(data, T, rate, iterations,airSpeed,airCriteria,airCost,carSpeed,carCost):

    bestCostPerIter = []
    coordinates = np.copy(data)
    currentGuess = pathGenerator(coordinates)
    currentCost,currentCostVec = timeCostCalc(currentGuess,airCriteria,airSpeed,airCost,carSpeed,carCost, "cost")
    #Determining the total distance and associated distance vector of the initial guess

    bestGuess = np.copy(currentGuess) #Determining a placeholder value for best guess
    bestCost, bestCostVec = timeCostCalc(bestGuess,airCriteria,airSpeed,airCost,carSpeed,carCost, "cost")
    
    #Using for loop to go through iterations specified in anneal function:
    for i in range(iterations):
        newGuess = pathGenerator(currentGuess)
        newCost,newCostVec = timeCostCalc(newGuess,airCriteria,airSpeed,airCost,carSpeed,carCost, "cost")
        if newCost < currentCost or random.random() < math.exp((currentCost - newCost)/T): 
            #Making acceptance decision based on acceptance probability
            currentGuess = newGuess
            currentCost = newCost #Swapping between current guess and new guess
            if newCost < bestCost:
                bestCost = currentCost
                bestCostVec = currentCostVec #Updating best guess if current guess is more optimal (less expensive)
        
        bestCostPerIter.append(bestCost) #Storing the best guess per iteration
        
        T = rate * T #Temperature decreases according to exponential rate
    return bestGuess, bestCost, bestCostPerIter

"""
annealOptimization is used to conveniently store all optimization features, and determines which one is being called. 
Multiple parameters are input to determine characteristics of air or land travel.

INPUTS
data: the path through which the salesman travels, which is a n by 2 numpy array
T: starting temperature of Simulated Annealing temperature function (exponential decay model)
rate: rate of temperature decay
iterations: number of iterations ran by simulated annealing optimization
airCriteria: maximum distance in miles salesman is willing to drive
airSpeed: average speed of air travel, measured in mph
airCost: cost of air travel, measured in dollars per hour
carSpeed: average speed of car travel, measured in mph
carCost: cost of car travel, measured in dollars per hour
optimizationType: used to switch between which values are returned by timeCostCalc
"time" returns time related information
"time" returns time related information
"cost" returns cost related information

OUTPUTS
return values given by simulated annealing functions
"""

def annealOptimization(data, T, rate, iterations,airSpeed,airCriteria,airCost,carSpeed,carCost, optimizationType):
    #Based on optimization 
    if optimizationType == "distance":
        return annealDistance(data, T, rate, iterations)
    elif optimizationType == "cost":
        return annealCost(data, T, rate, iterations,airSpeed,airCriteria,airCost,carSpeed,carCost)
    elif optimizationType == "time":
        return annealTime(data, T, rate, iterations,airSpeed,airCriteria,airCost,carSpeed,carCost)

"""
pathGrapher is used to plot optimal path determiend by Simulated Annealing method. 
Multiple parameters are input to determine visual characteristics.

INPUTS
data: the path through which the salesman travels, which is a n by 2 numpy array
lineColor: color of the path line
title: title of graph, to be displayed using plt.title()

OUTPUTS
NONE
"""

def pathGrapher(data, lineColor, title):
    dataLoop = np.vstack((data, data[0,:])) #In order for the full path to be graphed, the first data row must be put on the bottom of the data
    #In order for the path grapher to fully loop back to the initial value, the first row must be copied to the bottom
    x = dataLoop[:,0] #Extracting x and y data from the fully looped data
    y = dataLoop[:,1]
    plt.plot(x,y,alpha = 0.8,color=lineColor, label = "Optimized Path")
    plt.scatter(x,y, marker = ".", color="black", alpha = 1, label = "State Capitals")
    plt.plot(x[0], y[0], marker = "^",markersize = 10, color="orange", label = "Starting State Capital") #Starting city is denoted with special marker
    plt.xlabel("Latitude (deg.)")
    plt.ylabel("Longitude (deg.)")
    plt.legend()
    plt.title(title)
    plt.show()

"""
main function which contains three scenarios, with all values already preset.

SCENARIO 1: City Traveling

This scenario considers the 50 state capitals of the United States. Starting from a random city and given different initial parameters,
paths that optimize distance, time, and cost are generated and plotted. All important outputs, such as total distance, time, and cost are also printed. 
Graphs of best distance, time, and cost per iterations are also plotted. The last graph plotted is the relative optimiization performance of 
each iteration compared to the final best distance, time, and cost.

SCENARIO 2: Testing Convergence over Iteration Count 

This scenario considers the convergence of the Simulated Annealing algorithm over many iterations.

SCENARIO 3: Circle Traveling

This scenario considers travel across a circle. Starting from a random point along the circle, paths that optimize distance, time, and cost 
are generated and plotted along with the exact order of cities, and the total distance, time, and cost are printed. All important outputs, 
such as total distance, time, and cost are also printed. Compared to SCENARIO 1, SCENARIO 3 exaggerates the effect of which quantity is best optimized,
which is illustrated by the distinct changes in optimal path. 
-----

In order to activate a scenario, set its value below to True. If multiple scenarios are set at the same time, only the topmost one will run.

"""

if __name__ == "__main__":

    scenario1 = True
    scenario2 = True
    scenario3 = False

    T = 10000
    rate = 0.95
    iterations = 2000

    #######################################################################################
    #SCENARIO 1: Traveling Salesman State Capitals: Distance Optimization #################
    #######################################################################################

    airSpeed = 600 #mph
    airCriteria = 300 #maximum of 4 hour drive
    airCost = 10.0 #dollars
    carSpeed = 60 #mph
    carCost = 1 #dollars
    
    #Latitude Longitude Points of all US State Capitals
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
    (41.140259, -104.820236)])
    
    #######################################################################################
    
    #######################################################################################
    #SCENARIO 2: Testing Convergence Over Iterations ######################################
    #######################################################################################

    T = 10000000
    rate = 0.999
    airSpeed1 = 600 #mph
    airCriteria1 = 300 #maximum of 4 hour drive
    airCost1 = 10.0 #dollars
    carSpeed1 = 60 #mph
    carCost1 = 1 #dollars

    iterationRange = np.array([10,100,1000,10000,100000])#,,1000000]) 

    #There is significant computation needed past 10^6 iterations. As a result, that iteration number has been commented out.

    #######################################################################################

    #######################################################################################
    #SCENARIO 3: Traveling In Circles #####################################################
    #######################################################################################

    airSpeed = 500 #mph
    airCriteria = 300 #maximum of 4 hour drive
    airCost = 1 #dollars
    carSpeed = 70 #mph
    carCost = 3.0 #dollars

    radius = 1000
    points = 20 #Determines how many points will be on the circle.
    theta = np.linspace(0, 2 * np.pi, points)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    # Create the n by 2 array of points
    data2 = np.array([x, y]).T

    #######################################################################################

    if scenario1:

        print("SIMULATION RUNNING")

        #Performing optimization based on distance, time, and cost
        bestPath, bestDistance,bestDistancePerIter = annealOptimization(data,T,rate,iterations,airSpeed, airCriteria, airCost, carSpeed, carCost, "distance")
        bestTimePath, bestTime, bestTimePerIter = annealOptimization(data,T,rate,iterations,airSpeed, airCriteria, airCost, carSpeed, carCost, "time")
        bestCostPath, bestCost, bestCostPerIter = annealOptimization(data,T,rate,iterations,airSpeed, airCriteria, airCost, carSpeed, carCost, "cost")
        
        #Calculating optimization performance per iteration relative to final best optimized values
        relPerformDist = bestDistance/bestDistancePerIter
        relPerformTime = bestTime/bestTimePerIter
        relPerformCost = bestCost/bestCostPerIter

        print("SIMULATION RESULTS:")

        print("Optimal Distance:", bestDistance, "Miles")
        print("Optimal Time:", bestTime, "Hr")
        print("Optimal Cost:", bestCost, "USD")

        #The following graphs plot the final optimal paths

        pathGrapher(bestPath, "red", "Optimal Distance Path")
        pathGrapher(bestTimePath, "green", "Optimal Time Path")
        pathGrapher(bestCostPath, "blue", "Optimal Cost Path")

        #The following graphs plot the best distance per iteration

        plt.plot(bestDistancePerIter)
        plt.xlabel("Iteration Count")
        plt.ylabel("Total Cost (USD)")
        plt.title("Simulated Annealing Cost Performance over Iteration")
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

        plt.plot(relPerformDist, label = "Distance")
        plt.plot(relPerformCost, label = "Cost")
        plt.plot(relPerformTime, label = "Time")
        plt.xlabel("Iteration Count")
        plt.ylabel("Relative Performance (%)")
        plt.title("Relative Performance of Different Optimization Compared to Final Optimal Value")
        plt.legend()
        plt.show()        
    
    elif scenario2:

        bestDistancesTotal = np.zeros(len(iterationRange))
        for i in range(0,len(iterationRange)):
            #Performing optimization based on distance
            bestPath, bestDistance,bestDistancePerRun = annealOptimization(data,T,rate,iterationRange[i],airSpeed, airCriteria, airCost, carSpeed, carCost, "distance")
            bestDistancesTotal[i] = bestDistance
            print("N = %f Cycle Complete" %iterationRange[i])
        
        plt.loglog(iterationRange,bestDistancesTotal)
        plt.xlabel("Iteration Number")
        plt.ylabel("Best Distance (mi)")
        plt.title("Relationship between Best Distance and Iteration Number")
        plt.show()

    elif scenario3:

        print("SIMULATION RUNNING")

        #Performing optimization based on distance, time, and cost

        bestPath, bestDistance,bestDistancePerIter = annealOptimization(data,T,rate,iterations,airSpeed, airCriteria, airCost, carSpeed, carCost, "distance")
        bestTimePath, bestTime, bestTimePerIter = annealOptimization(data,T,rate,iterations,airSpeed, airCriteria, airCost, carSpeed, carCost, "time")
        bestCostPath, bestCost, bestCostPerIter = annealOptimization(data,T,rate,iterations,airSpeed, airCriteria, airCost, carSpeed, carCost, "cost")

        print("SIMULATION RESULTS:")

        print("Optimal Distance:", bestDistance, "Miles")
        print("Optimal Time:", bestTime, "Hr")
        print("Optimal Cost:", bestCost, "USD")

        pathGrapher(bestPath, "red", "Optimal Distance Path")
        pathGrapher(bestTimePath, "green", "Optimal Time Path")
        pathGrapher(bestCostPath, "blue", "Optimal Cost Path")   
