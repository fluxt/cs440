import numpy as np
import utils
import heapq
import astar
from collections import defaultdict

class Node():
	def __init__(self, position, collected):
		self.pos = position
		self.collected = collected

	def __gt__(self, other):
		return True

	def __str__(self):
		return ("pos=" + str(self.pos) + "\ncollected=" + str(self.collected))


grid, simple_graph, pacman_position, goal_positions = utils.load_puzzle("part1/bigDots.txt")
num_goals = len(goal_positions)
init_node = Node(pacman_position, [False for p in goal_positions])
x_size, y_size = grid.shape

goal_distances = np.zeros((num_goals, num_goals))
for i in range(len(goal_positions) - 1):
	for j in range(i+1, len(goal_positions)):
		dist = len(astar.a_star(simple_graph, goal_positions[i], goal_positions[j]))
		goal_distances[i][j] = dist
		goal_distances[j][i] = dist
print("Done with preprocessing")


def manhattan_dist(pos1, pos2):
	return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


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
				#edges.append((adj_matrix[vertex][r], vertex, r))
				heapq.heappush(edges, (adj_matrix[vertex][r], vertex, r))

		while not min_edge:
			min_edge = heapq.heappop(edges)
			if (min_edge[2] in visited):
				min_edge = None
		#min_edge = min(edges, key=lambda x: 10000 if x[2] in visited else x[0])
		#edges.remove(min_edge)

		MST.add(min_edge)
		vertex = min_edge[2]
		min_edge = None

	return sum([e[0] for e in MST])


def heuristic_cost_estimate(node):
	#return max(node.collected.count(False), max([manhattan_dist(g, node.pos) for g in goal_positions]))

	return node.collected.count(False) * 10

	#all_nodes = [goal_positions[i] for i in range(len(goal_positions)) if not node.collected[i]]
	#all_nodes.append(node.pos)

	#if (len(all_nodes) == 1):
	#	return 0
	#return sum([min([taxi_dist_or_inf(n1, n2) for n2 in all_nodes]) for n1 in all_nodes]) / 2

	#graph = np.array([[manhattan_dist(pos1, pos2) for pos2 in all_nodes] for pos1 in all_nodes])

#	uncollected_indices = [i for i in range(len(goal_positions)) if not node.collected[i]]
#	graph = np.zeros((len(uncollected_indices) + 1, len(uncollected_indices) + 1), dtype=int)

#	for i in range(len(uncollected_indices)):
#		for j in range(i+1, len(uncollected_indices)):
#			graph[i][j] = goal_distances[uncollected_indices[i]][uncollected_indices[j]]
#			graph[j][i] = goal_distances[uncollected_indices[i]][uncollected_indices[j]]

#		graph[i][len(uncollected_indices)] = manhattan_dist(node.pos, goal_positions[uncollected_indices[i]])
#		graph[len(uncollected_indices)][i] = manhattan_dist(node.pos, goal_positions[uncollected_indices[i]])

#	return mst_size(graph)


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


def multiple_goal_a_star():
	closed_set = set()

	open_set_heap = [(10000 ,init_node)]
	open_set_set = {init_node}

	came_from = dict()

	g_score_dict = defaultdict(lambda: 10000)
	f_score_dict = defaultdict(lambda: 10000)

	g_score_dict[init_node] = 0

	collected = 0

	path = []

	while(open_set_heap):
		current = heapq.heappop(open_set_heap)[1]
		open_set_set.remove(current)

		curr_coll = current.collected.count(True)
		if (curr_coll > collected):
			print(curr_coll)
			print(current.pos)
			collected = curr_coll

		if (is_finished(current)):
			path.append(current.pos)
			break

		closed_set.add(current)

		for neighbor in get_neighbors(current):
			if neighbor in closed_set:
				continue

			tentative_g_score = g_score_dict[current] + 1
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


if __name__ == "__main__":
	path = multiple_goal_a_star()

	utils.draw_solution_to_grid(grid, path)
	utils.print_grid(grid)
	print("Path: " + str(path))
	print("Length of path: " + str(len(path)))
