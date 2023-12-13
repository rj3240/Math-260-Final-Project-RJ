# Ravi Jain: Math 260 Final Project
## Simulated Annealing Optimization Methods: The Traveling Salesman Problem

### Simulated Annealing: Introduction

Simulated Annealing is an optimization method used to determine the global maximum or minimum of a data set (). It differs from other optimization techniques such as gradient descent methods in its usage of a dynamically changing heat factor. Simulated Annealing mirrors the real life dynamics of annealing, where a metal is brought to high temperatures and slowly brought to a lower steady state temperature (Baird). When the system is initially unordered (temperature is very high), the optimization algorithm has a relatively high probability to accept a worse solution than the current best solution (Baird). As temperature decreases, the probability of accepting a worse solution approaches zero, and the system reaches equilibrium (Carr).

While all optimization methods are prone to local extrema, the Simulated Annnealing method is unique in its iteration-dependent acceptance probabiltiies. Analagous to real annealing, the probability that the algorithm will choose a new solution is dependent on the temperature of the system (Carr). By allowing for different solutions to be accepted when the system temperature is high, the algorithm is able to unroot itself from any local extrema points (Carr). When tackling discrete problems with multiple peaks, Simulated Annealing's ability to escape local extrema becomes very useful. In comparison, an optimization method such as gradient descent would have much more trouble escaping a local extrema point due to its dependence on slope. Likewise, any form of hill climbing optimization would be trapped in a local extrema point—as the algorithm terminates once better neighbors aren't found, it has no way of discerning between global and local extrem and can be easily misled. 

### Simulated Annealing: Discrete Problems and the Traveling Salesman 

One optimization problem Simulated Annealing can be used to great effect is the Traveling Salesman problem. The traveling salesmen problem asks the following question: given N points, what is the shortest route that connects all points and returns to the initial starting point. In the traveling salesmen problem, this question is rephrased into the following: given N cities, what is the shortest route that a traveling salesman can take to go to each city exactly once and return to their original starting city. These cities are represented using coordinates, which allows for optimization in two, three, or n-dimensions.

For this project, I decided to optimize travel routes between the 50 state capitals of the United States. Along with optimizing distance, I also decided to optimize other quantities, such as route's total time along with the route's total cost. These quantities were determined based on the distance between state capitals (which would be converted into required time for travel and cost for travel).

### Simulated Annealing: Use Instructions and Notes

The following code has three scenarios provided. Scenario 1 is the traveling salesman problem solved for the above situation. Scenario 2 tests the convergence of optimal solutions as iteration number increases. Scenario 3 is the traveling salesmen problem solved for a distribution of points in a circle. This scenario is useful in showcasing how adjustment of cost and time parameters can result in drastically different optimal routes, which is somewhat hard to see with scenario 1. Scenario 4 showcases the performance of simulated annealing models for large number of points, solving the traveling salesman problem for a set of 500 points randomly distributed in a 10000 by 10000 square.   

Each scenario has its own set of parameters that can be separately adjusted per scenario. Placeholder values have already been added in the code file, and can be changed based on the user's specifications. On the other hand, parameters controlling iteration, temperature, and temperature rate are global across all scenarios. They should be changed depending on which scenario is active. Below are some useful tips:

1. If running scenario 1, a good iteration number to use is around 30000. If a lower iteration number is used (such as 10000), the optimization is more likely to be caught in a local extrema point.
1. If running scenario 4, ensure that the temperature is around 10000000, rate is around 0.995, and the iteration number is low (approx. 20000). Otherwise, the program will take a significantly long time to finish running.
1. Generally, if one runs a higher iteration number, temperature or rate should also increase. This is to prevent any possibility of the temperature becoming so low that a floating point error emerges.

Everytime a scenario runs, a matplotlib window will open and plot the results of the scenario. If you cannot see these results, a folder of all plots is provided in the github repository. If the user wants to access the full data set used for scenario 1, "us-state-capitals.csv" has all coordinate information. For this code, all coordinate data has been already loaded, so the program will still work even if there are issues with the repository and csv file.

### Citations:

Baird, Leemon. “Simulated Annealing.” Auton Project at CMU, www.cs.cmu.edu/afs/cs.cmu.edu/project/learn-43/lib/photoz/.g/web/glossary/anneal.html. Accessed 13 Dec. 2023. 

Carr, Roger. "Simulated Annealing." From MathWorld--A Wolfram Web Resource, created by Eric W. Weisstein. https://mathworld.wolfram.com/SimulatedAnnealing.html. Accessed 13 Dec. 2023.

State capital data provided by Jasper Debie. https://github.com/jasperdebie/VisInfo/blob/master/us-state-capitals.csv
