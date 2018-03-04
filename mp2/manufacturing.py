from collections import defaultdict
import time

distances =[[0, 1064, 673, 1401, 277],
	[1064, 0, 958, 1934, 337],
	[673, 958, 0, 1001, 399],
	[1401, 1934, 1001, 0, 387],
	[277, 337, 399, 387, 0]]

reduced_distances = [[0, 614, 673, 664, 277], 
		[614, 0, 776, 764, 337],
		[673, 776, 0, 786, 399],
		[664, 764, 776, 0, 387],
		[277, 337, 399, 387, 0]]

#A=0, B=1, C=2, D=3, E=4

widget_orders =[[0, 4, 3, 2, 0, -1],
		[1, 4, 0, 2, 3, -1],
		[1, 0, 1, 2, 4, -1],
		[3, 0, 3, 1, 3, -1],
		[1, 4, 2, 1, 3, -1]]

# each node represents a different state
class Node():
	def __init__(self, progress, location):
		self.progress = progress
		self.location = location

	def __eq__(self, other):
		return self.progress == other.progress and self.location == other.location

	def __hash__(self):
		return hash((self.progress, self.location))

	def __str__(self):
		return "Progress: " + str(self.progress) + ", Location: " + str(self.location)
	
	def __gt__(self, other):
		return True

def get_min_path_cost(path):
	cost = 0
	for i in range(len(path) - 1):
		cost += reduced_distances[path[i]][path[i+1]]
	return cost

# our heuristic function for A-Star
def heuristic_cost_estimate_1(node):
	return 5 - min(node.progress)

def heuristic_cost_estimate_2(node):
	#return 0

	max_total = 0
	for i in range(5):
		widget_prog = node.progress[i]
		path = [node.location]
		path.extend(widget_orders[i][widget_prog:6])
		total = get_min_path_cost(path)
		if total > max_total:
			max_total = total
	return max_total

def distance_step_cost(node1, node2):
	if node1.location == -1 or node2.location == -1:
		return 0
	return distances[node2.location][node1.location]

# get a list of the other nodes that can be reached from a node
def get_neighbors(node):
	ret = []
	for next_loc in range(5):
		new_prog = [0 for n in range(5)]
		for widget_idx in range(5):
			if next_loc == widget_orders[widget_idx][node.progress[widget_idx]]:
				new_prog[widget_idx] = node.progress[widget_idx] + 1
			else:
				new_prog[widget_idx] = node.progress[widget_idx]
		ret.append(Node(tuple(new_prog), next_loc))
	return ret

# check if a node has finished its journey
def is_finished(node):
	return node.progress.count(5) == 5

def a_star(init_node, heuristic, step_cost):
	# a set of nodes we have already expanded
	closed_set = set()

	# open set (nodes we have seen, but not expanded)
	open_set = {init_node}

	# a dictionary that maps nodes to the node that they came from. used for reconstructing the path at the end
	came_from = dict()

	# a map from a node to the distance from the start to that node
	g_score_dict = defaultdict(lambda: float("inf"))

	# a map from a node to the distance from the start plus the heuristic distance to the end
	f_score_dict = defaultdict(lambda: float("inf"))

	g_score_dict[init_node] = 0

	path = []

	while(open_set):
		# remove the node with the smallest f_score
		current = min(open_set, key= lambda x: f_score_dict[x])
		open_set.remove(current)

		# if current is done, then break
		if (is_finished(current)):
			path.append(current.location)
			break

		closed_set.add(current)

		for neighbor in get_neighbors(current):
			if neighbor in closed_set:
				continue

			# get the new g_score for this node
			tentative_g_score = g_score_dict[current] + step_cost(current, neighbor)
			if tentative_g_score < g_score_dict[neighbor]:
				came_from[neighbor] = current
				g_score_dict[neighbor] = tentative_g_score
				f_score_dict[neighbor] = tentative_g_score + heuristic(neighbor)

			if neighbor not in open_set:
				open_set.add(neighbor)

	# recreate the path from the came_from map
	while current in came_from:
		current = came_from[current]
		path.append(current.location)

	path.reverse()
	# return  the path and the number of nodes expanded
	return path[1:], len(closed_set)

def get_path_cost(path):
	cost = 0
	for i in range(len(path) - 1):
		cost += distances[path[i]][path[i+1]]
	return cost

if __name__ == "__main__":
	start_1 = time.time()

	init_node_1 = Node((0, 0, 0, 0, 0), -1)

	print("PART 1")
	path_1, nodes_expanded_1 = a_star(init_node_1, heuristic_cost_estimate_1, lambda x,y: 1)

	print("path cost is  : ", len(path_1))
	print("path: ", str(path_1))
	print("nodes expanded: ", nodes_expanded_1)
	end_1 = time.time()
	print("total runtime : {0:.3f} seconds".format(end_1-start_1))
	print()

	start_2 = time.time()
	init_node_2 = Node((0, 0, 0, 0, 0), -1)

	print("PART 2")
	path_2, nodes_expanded_2 = a_star(init_node_2, heuristic_cost_estimate_2, distance_step_cost)

	print("path cost is  : ", get_path_cost(path_2))
	print("path: ", str(path_2))
	print("nodes expanded: ", nodes_expanded_2)
	end_2 = time.time()
	print("total runtime : {0:.3f} seconds".format(end_2-start_2))

