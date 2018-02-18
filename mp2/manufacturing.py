import numpy as np
import utils
import heapq
import astar
from collections import defaultdict
import time

# each node represents a different state: includes a list for goals collectd so far and an integer for the position pacman is at now
class Node():
	def __init__(self, position, collected):
		# collected should be a list of boolean values for each goal position
		self.collected = collected
		# position should be an integer representing the an index of goal_positions
		self.pos = position

	def __gt__(self, other):
		return True

# our heuristic function for A-Star
def heuristic_cost_estimate(node, goal_distances):
	num_goals = goal_distances.shape[0]

	# a list of the indices of the goal_positions that have not yet been collected
	uncollected_indices = [i for i in range(num_goals) if not node.collected[i]]

	# add the current position becayse we need it to be part of the MST
	uncollected_indices.append(node.pos)

	# set up an adjacency matrix only including uncollected_indices
	graph = np.zeros((len(uncollected_indices), len(uncollected_indices)), dtype=int)

	for i in range(len(uncollected_indices) - 1):
		for j in range(i+1, len(uncollected_indices)):
			graph[i][j] = goal_distances[uncollected_indices[i]][uncollected_indices[j]]
			graph[j][i] = goal_distances[uncollected_indices[i]][uncollected_indices[j]]

	# return the total edge weights of a mst of this graph
	return mst_size(graph)

# get a list of the other nodes that can be reached from a node
def get_neighbors(node):
	

# check if a node has finished its journey
def is_finished(node):
	return node.collected.count(False) == 0

def a_star(goal_positions, init_node, goal_distances):
	# a set of nodes we have already expanded
	closed_set = set()

	# open set (nodes we have seen, but not expanded)
	# we store this as a paralell min-heap and set for better efficiency
	open_set_heap = [(heuristic_cost_estimate(init_node, goal_distances) ,init_node)]
	open_set_set = {init_node}

	# a dictionary that maps nodes to the node that they came from. used for reconstructing the path at the end
	came_from = dict()

	# a map from a node to the distance from the start to that node
	g_score_dict = defaultdict(lambda: 10000)

	# a map from a node to the distance from the start plus the heuristic distance to the end
	f_score_dict = defaultdict(lambda: 10000)

	g_score_dict[init_node] = 0

	path = []

	while(open_set_heap):
		# remove the node with the smallest f_score
		current = heapq.heappop(open_set_heap)[1]
		open_set_set.remove(current)

		# if current is done, then break
		if (is_finished(current)):
			path.append(current.pos)
			break

		closed_set.add(current)

		for neighbor in get_neighbors(current):
			if neighbor in closed_set:
				continue

			# get the new g_score for this node
			tentative_g_score = g_score_dict[current] + goal_distances[neighbor.pos][current.pos]
			if tentative_g_score < g_score_dict[neighbor]:
				came_from[neighbor] = current
				g_score_dict[neighbor] = tentative_g_score
				f_score_dict[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor, goal_distances)

			if neighbor not in open_set_set:
				open_set_set.add(neighbor)
				heapq.heappush(open_set_heap, (f_score_dict[neighbor] ,neighbor))

	# recreate the path from the came_from map
	while current in came_from:
		current = came_from[current]
		path.append(current.pos)

	path.reverse()
	# return  the path and the number of nodes expanded
	return path, len(closed_set)

if __name__ == "__main__":
	for fileName in ["part1/tinySearch.txt", "part1/smallSearch.txt", "part1/mediumSearch.txt"]:
		start = time.time()
		grid, goal_positions, init_node, goal_distances = load_tsp(fileName)
		path, nodes_expanded = multiple_goal_a_star(goal_positions, init_node, goal_distances)

		put_path_on_grid(path, grid)
		utils.print_grid(grid)
		print("path cost is  : ", get_path_cost(path, goal_distances))
		print("nodes expanded: ", nodes_expanded)
		end = time.time()
		print("total runtime : {0:.3f} seconds".format(end-start))
		print()
