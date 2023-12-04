import numpy as np
import math
import random
import matplotlib.pyplot as plt

def calculate_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def calculate_total_distance(route, coordinates):
    total_distance = 0
    num_cities = len(route)
    
    for i in range(num_cities - 1):
        total_distance += calculate_distance(coordinates[route[i]], coordinates[route[i + 1]])
    
    # Return to the starting city
    total_distance += calculate_distance(coordinates[route[-1]], coordinates[route[0]])
    
    return total_distance

def generate_initial_solution(num_cities):
    return random.sample(range(num_cities), num_cities)

def swap_cities(route):
    # Randomly swap two cities in the route
    new_route = route.copy()
    i, j = random.sample(range(len(route)), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

def plot_tsp_solution(coordinates, route):
    # Plot the TSP solution
    x = [coordinates[city][0] for city in route]
    y = [coordinates[city][1] for city in route]

    plt.plot(x, y, 'o-', markersize=8, label='Path')
    plt.scatter(x, y, color='red', label='Cities')

    plt.title('Traveling Salesman Problem Solution')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.legend()
    plt.show()

def simulated_annealing_tsp(coordinates, initial_temperature, cooling_rate, num_iterations):
    num_cities = len(coordinates)
    current_route = generate_initial_solution(num_cities)
    current_distance = calculate_total_distance(current_route, coordinates)
    best_route = current_route.copy()
    best_distance = current_distance

    distance_history = []

    for iteration in range(num_iterations):
        temperature = initial_temperature * (cooling_rate ** iteration)
        new_route = swap_cities(current_route)
        new_distance = calculate_total_distance(new_route, coordinates)

        # Metropolis criterion
        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temperature):
            current_route = new_route
            current_distance = new_distance

            # Update the best solution if needed
            if current_distance < best_distance:
                best_route = current_route
                best_distance = current_distance

        distance_history.append(best_distance)

    return best_route, best_distance, distance_history

# Example usage
# Replace this with your actual coordinates and parameters.
city_coordinates = np.array([[0,100],[100,0],[-100,0],[0,-100],[0,200],[200,0],[-200,0],[0,-200],[0,300],[300,0],[-300,0],[0,-300] ])

initial_temperature = 1000.0
cooling_rate = 0.995
iterations = 1000

best_route, best_distance, distance_history = simulated_annealing_tsp(city_coordinates, initial_temperature, cooling_rate, iterations)

print("Best Route:", best_route)
print("Best Distance:", best_distance)

# Plotting the TSP solution
plot_tsp_solution(city_coordinates, best_route)

# Plotting the convergence of the algorithm
plt.plot(distance_history)
plt.title('Convergence of Simulated Annealing for TSP')
plt.xlabel('Iteration')
plt.ylabel('Best Distance')
plt.show()
