import heapq
from collections import defaultdict
import time

distances =[[0, 1064, 673, 1401, 277],
	[1064, 0, 958, 1934, 337],
	[673, 958, 0, 1001, 399],
	[1401, 1934, 1001, 0, 387],
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

	def __str__(self):
		return "Progress: " + str(self.progress) + ", Location: " + str(self.location)
	
	def __gt__(self, other):
		return True

# our heuristic function for A-Star
def heuristic_cost_estimate(node):
	return 5 - min(node.progress)

# get a list of the other nodes that can be reached from a node
def get_neighbors(node):
	ret = []
	for next_loc in range(5):
		new_prog = [0 for n in range(5)]
		for widget_idx in range(5):
			if next_loc == widget_orders[widget_idx][node.progress[widget_idx] + 1]:
				new_prog[widget_idx] = node.progress[widget_idx] + 1
			else:
				new_prog[widget_idx] = node.progress[widget_idx]
		ret.append(Node(tuple(new_prog), next_loc))
	return ret

# check if a node has finished its journey
def is_finished(node):
	return node.progress.count(5) == 5

def a_star(init_node):
	# a set of nodes we have already expanded
	closed_set = set()

	# open set (nodes we have seen, but not expanded)
	# we store this as a paralell min-heap and set for better efficiency
	open_set_heap = [(heuristic_cost_estimate(init_node) ,init_node)]
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

		print(current)

		# if current is done, then break
		if (is_finished(current)):
			path.append(current.pos)
			break

		closed_set.add(current)

		for neighbor in get_neighbors(current):
			if neighbor in closed_set:
				print(neighbor)
				continue

			# get the new g_score for this node
			tentative_g_score = g_score_dict[current] + 1

			if tentative_g_score < g_score_dict[neighbor]:
				came_from[neighbor] = current
				g_score_dict[neighbor] = tentative_g_score
				f_score_dict[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor)

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
	start = time.time()

	init_node = Node((0, 0, 0, 0, 0), -1)
	path, nodes_expanded = a_star(init_node)

	put_path_on_grid(path, grid)
	utils.print_grid(grid)
	print("path cost is  : ", len(path))
	print("path: ", str(path))
	print("nodes expanded: ", nodes_expanded)
	end = time.time()
	print("total runtime : {0:.3f} seconds".format(end-start))
	print()
