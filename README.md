# Ravi Jain: Math 260 Final Project
## Simulated Annealing Optimization Methods: The Traveling Salesman Problem

### Simulated Annealing: Introduction

Simulated Annealing is an optimization method used to determine the global maximum or minimum of a data set. It differs from other optimization techniques such as gradient descent methods in its usage of a dynamically changing heat factor. Simulated Annealing mirrors the real life dynamics of annealing, where a metal is brought to high temperatures and slowly brought to a lower steady state temperature. When the system is initially unordered (temperature is very high), the optimization algorithm has a relatively high probability to accept a worse solution than the current best solution. As temperature decreases, the probability of accepting a worse solution approaches zero, and the system reaches equilibrium.

While all optimization methods are prone to local extrema, the Simulated Annnealing method is unique in its iteration-dependent acceptance probabiltiies. Analagous to real annealing, the probability that the algorithm will choose a new solution is dependent on the temperature of the system. By allowing for different solutions to be accepted when the system temperature is high, the algorithm is able to unroot itself from any local extrema points. When tackling discrete problems with multiple peaks, Simulated Annealing's ability to escape local extrema becomes very useful. In comparison, an optimization method such as gradient descent would have much more trouble escaping a local extrema point due to its dependence on slope. Likewise, any form of hill climbing optimization would be trapped in a local extrema point—as the algorithm terminates once better neighbors aren't found, it has no way of discerning between global and local extrem and can be easily misled. 


### Simulated Annealing: Discrete Problems and the Traveling Salesman 