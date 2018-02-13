import numpy as np
import utils
import heapq
import astar
from collections import defaultdict
import time


# start by making the graph of distances between each goal position
def load_tsp(fileName):
	grid, simple_graph, pacman_position, goal_positions = utils.load_puzzle(fileName)
	# assume there is another goal underneath pacman's original position. This will not affect how the code runs, but it does make the starting configuration easier to handle
	goal_positions.append(pacman_position)
	num_goals = len(goal_positions)

	# a 2-D array of the shortest distances between each pair of goal positions
	goal_distances = np.zeros((num_goals, num_goals), dtype=int)
	for i in range(num_goals):
		for j in range(i+1, num_goals):
			dist = len(astar.a_star(simple_graph, goal_positions[i], goal_positions[j])[0]) - 1
			goal_distances[i][j] = dist
			goal_distances[j][i] = dist
		# make a high cost to travel from a node to itself, since we do not want this to happen
		goal_distances[i][i] = 1000

	return grid, goal_positions, goal_distances

def multiple_nearest_neighbor(goal_positions, goal_distances):
	uncollected = [i for i in range(len(goal_positions)-1)]
	# the most hackish shit I have ever done
	source = len(goal_positions)-1
	path = [source]
	nodes_expanded = 0
	while uncollected:
		minimum_distance = 10000
		# search which goal is closest
		for uncollected_index in uncollected:
			distance = goal_distances[source][uncollected_index]
			if distance < minimum_distance:
				destination = uncollected_index
				minimum_distance = distance
		# remove the closest node from uncollected, set source, and set path
		uncollected.remove(destination)
		source = destination
		path.append(destination)
		nodes_expanded += 1

	return path, nodes_expanded

# change the grid to have the dots numbered/lettered
def put_path_on_grid(path, grid):
	for i in range(1, len(path)):
		pos = goal_positions[path[i]]
		grid[pos[0]][pos[1]] = chr(i + 48) if i < 10 else chr(i + 87)

# given a path (a list of indices of goal_positions), return the total cost of this path
def get_path_cost(path, goal_distances):
	return sum([goal_distances[path[i]][path[i+1]] for i in range(len(path) - 1)])

if __name__ == "__main__":
	for fileName in ["part1/tinySearch.txt", "part1/smallSearch.txt", "part1/mediumSearch.txt", "part1/bigDots.txt"]:
		start = time.time()
		grid, goal_positions, goal_distances = load_tsp(fileName)
		path, nodes_expanded = multiple_nearest_neighbor(goal_positions, goal_distances)

		# big dots cannot correctly represented
		if fileName != "part1/bigDots.txt":
			put_path_on_grid(path, grid)
			utils.print_grid(grid)
		print("path cost is  : ", get_path_cost(path, goal_distances))
		print("nodes expanded: ", nodes_expanded)
		end = time.time()
		print("total runtime : {0:.3f} seconds".format(end-start))
		print()
