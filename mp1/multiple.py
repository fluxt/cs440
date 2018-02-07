import numpy as np
import utils
import heapq
import astar
from collections import defaultdict

class Node():
	def __init__(self, position, collected):
		self.collected = collected
		self.pos = position

	def __gt__(self, other):
		return True

	def __str__(self):
		return ("pos = " + str() + "collected=" + str(self.collected))

# assume there is another goal underneath pacman's original position
grid, simple_graph, pacman_position, goal_positions = utils.load_puzzle("part1/tinySearch.txt")
goal_positions.append(pacman_position)
num_goals = len(goal_positions)
init_node = Node(num_goals - 1, [False for p in goal_positions if goal_positions != pacman_position])

goal_distances = np.zeros((num_goals, num_goals), dtype=int)
for i in range(num_goals):
	for j in range(i+1, num_goals):
		dist = len(astar.a_star(simple_graph, goal_positions[i], goal_positions[j])[0]) - 1
		goal_distances[i][j] = dist
		goal_distances[j][i] = dist
	goal_distances[i][i] = 1
print(goal_distances)
print("Done with preprocessing")


def mst_size(adj_matrix):
	vertex = 0
	num_nodes = adj_matrix.shape[0]

	MST = set()
	edges = []
	visited = set()
	min_edge = None

	while len(MST) != num_nodes - 1:
		visited.add(vertex)

		for r in range(num_nodes):
			if r != vertex:
				heapq.heappush(edges, (adj_matrix[vertex][r], vertex, r))

		while not min_edge:
			min_edge = heapq.heappop(edges)
			if (min_edge[2] in visited):
				min_edge = None

		MST.add(min_edge)
		vertex = min_edge[2]
		min_edge = None

	return sum([e[0] for e in MST])


def heuristic_cost_estimate(node):
	uncollected_indices = [i for i in range(num_goals) if not node.collected[i]]
	uncollected_indices.append(node.pos)
	graph = np.zeros((len(uncollected_indices), len(uncollected_indices)), dtype=int)

	for i in range(len(uncollected_indices) - 1):
		for j in range(i+1, len(uncollected_indices)):
			graph[i][j] = goal_distances[uncollected_indices[i]][uncollected_indices[j]]
			graph[j][i] = goal_distances[uncollected_indices[i]][uncollected_indices[j]]

	return mst_size(graph)


def get_neighbors(node):
	ret = []
	uncollected_indices = [i for i in range(num_goals) if not node.collected[i]]
	for i in uncollected_indices:
		new_collected = [True if i == node.pos else node.collected[i]  for i in range(num_goals)]
		ret.append(Node(i, new_collected))
	return ret


def is_finished(node):
	return node.collected.count(False) == 0

def multiple_goal_a_star():
	closed_set = set()

	open_set_heap = [(10000 ,init_node)]
	open_set_set = {init_node}

	came_from = dict()

	g_score_dict = defaultdict(lambda: 10000)
	f_score_dict = defaultdict(lambda: 10000)

	g_score_dict[init_node] = 0

	path = []

	while(open_set_heap):
		current = heapq.heappop(open_set_heap)[1]
		open_set_set.remove(current)

		if (is_finished(current)):
			path.append(current.pos)
			break

		closed_set.add(current)

		for neighbor in get_neighbors(current):
			if neighbor in closed_set:
				continue

			tentative_g_score = g_score_dict[current] + goal_distances[neighbor.pos][current.pos]
			if tentative_g_score < g_score_dict[neighbor]:
				came_from[neighbor] = current
				g_score_dict[neighbor] = tentative_g_score
				f_score_dict[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor)

			if neighbor not in open_set_set:
				open_set_set.add(neighbor)
				heapq.heappush(open_set_heap, (f_score_dict[neighbor] ,neighbor))

	while current in came_from:
		current = came_from[current]
		path.append(current.pos)
	print("Nodes expanded: " + str(len(closed_set)))

	path.reverse()
	return path

def put_path_on_grid(path):
	for i in range(1, len(path)):
		pos = goal_positions[path[i]]
		grid[pos[0]][pos[1]] = chr(i + 48) if i < 10 else chr(i + 87)

def print_path(path):
	print('Path: ' + str([goal_positions[i] for i in path]))

def get_path_cost(path):
	return sum([goal_distances[path[i]][path[i+1]] for i in range(len(path) - 1)])

if __name__ == "__main__":
	path = multiple_goal_a_star()

	#print(grid)
	put_path_on_grid(path)
	utils.print_grid(grid)
	print_path(path)
	print(get_path_cost(path))
