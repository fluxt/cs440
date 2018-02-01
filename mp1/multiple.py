import numpy as np
import utils

from collections import defaultdict

class Node():
	def __init__(self, position, collected):
		self.pos = position
		self.collected = collected

#	def __repr__(self):
#		return ("pos=" + str(self.pos + "\ncollected=" + str(self.collected))
	def __str__(self):
		return ("pos=" + str(self.pos) + "\ncollected=" + str(self.collected))


grid, _, pacman_position, goal_positions = utils.load_puzzle("part1/tinySearch.txt")#("part1/tinySearch.txt")
init_node = Node(pacman_position, [False for p in goal_positions])
x_size, y_size = grid.shape

def taxi_dist(pos1, pos2):
	return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def taxi_dist_or_inf(pos1, pos2):
	dist = taxi_dist(pos1, pos2)
	return dist if dist > 0 else 10000

def mst_size(adj_matrix):
	vertex = 0
	num_nodes = adj_matrix.shape[0]

	MST = set()
	edges = []
	visited = set()

	while len(MST) != num_nodes - 1:
		visited.add(vertex)

		for r in range(num_nodes):
			if r != vertex:
				edges.append((vertex, r, adj_matrix[vertex][r]))

		min_edge = min(edges, key=lambda x: 10000 if x[1] in visited else x[2])

		edges.remove(min_edge)
		MST.add(min_edge)
		vertex = min_edge[1]

	return sum([e[2] for e in MST])

def heuristic_cost_estimate(node):
	#return max(node.collected.count(False), max([taxi_dist(g, node.pos) for g in goal_positions]))
	#return node.collected.count(False)
	all_nodes = [goal_positions[i] for i in range(len(goal_positions)) if not node.collected[i]]
	all_nodes.append(node.pos)
	graph = np.array([[taxi_dist(pos1, pos2) for pos2 in all_nodes] for pos1 in all_nodes])
	return mst_size(graph)

	#if (len(all_nodes) == 1):
	#	return 0
	#return sum([min([taxi_dist_or_inf(n1, n2) for n2 in all_nodes]) for n1 in all_nodes]) / 2

def get_neighbors(node):
	x, y = node.pos
	ret = []
	# right
	if (x+1) < x_size and grid[x+1][y] != '%':
		n = Node((x+1, y), [True if goal_positions[i] == (x+1, y) else node.collected[i] for i in range(len(goal_positions))])
		ret.append(n)
	# left
	if (x-1) >= 0 and grid[x-1][y] != '%':
		n = Node((x-1, y), [True if goal_positions[i] == (x-1, y) else node.collected[i] for i in range(len(goal_positions))])
		ret.append(n)	
	# down
	if (y+1) < y_size and grid[x][y+1] != '%':
		n = Node((x, y+1), [True if goal_positions[i] == (x, y+1) else node.collected[i] for i in range(len(goal_positions))])
		ret.append(n)
	# up
	if (y-1) >= 0 and grid[x][y-1] != '%':
		n = Node((x, y-1), [True if goal_positions[i] == (x, y-1) else node.collected[i] for i in range(len(goal_positions))])
		ret.append(n)

	return ret

def is_finished(node):
	return node.collected.count(False) == 0

def a_star():
	closed_set = set()
	open_set = {init_node}
	came_from = dict()

	g_score_dict = defaultdict(lambda: 10000)
	f_score_dict = defaultdict(lambda: 10000)

	g_score_dict[init_node] = 0

	collected = 0

	path = []

	while(open_set):
		#current = min(open_set, key=f_score)
		current = min(open_set, key=lambda x : f_score_dict[x])
		curr_coll = current.collected.count(True)
		if (curr_coll > collected):
			print(curr_coll)
			collected = curr_coll
		if (is_finished(current)):
			path.append(current.pos)
			break

		open_set.remove(current)
		closed_set.add(current)

		for neighbor in get_neighbors(current):
			if neighbor in closed_set:
				continue

			if neighbor not in open_set:
				open_set.add(neighbor)

			tentative_g_score = g_score_dict[current] + 1
			if tentative_g_score < g_score_dict[neighbor]:
				came_from[neighbor] = current
				g_score_dict[neighbor] = tentative_g_score
				f_score_dict[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor)

	while current in came_from:
		current = came_from[current]
		path.append(current.pos)
	print(len(closed_set))

	path.reverse()
	return path

if __name__ == "__main__":
	path = a_star()

	utils.draw_solution_to_grid(grid, path)
	utils.print_grid(grid)
	print(len(path))
