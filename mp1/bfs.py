import numpy as np
import utils
from collections import defaultdict


def bfs(graph, pacman_pos, goal_position):
	# dictionary of nodes visited
	distance = {node:None for node in graph}
	distance[pacman_pos] = 0
	# dictionary of node's parents
	parent = defaultdict(lambda: None)
	# push start position into the queue (list)
	queue = [pacman_pos]
	nodes_expanded = 0
	while queue:
		 	# pop the first element from the queue
			coordinate = queue.pop(0)
			nodes_expanded += 1
			# if the current coordinate is equivalent to the end position exit the while loop and return shortest path
			if coordinate == goal_position:
				break
			# loop through all of the neighbors within the current coordinate in the graph
			for vertex in graph[coordinate]:
				if distance[vertex] is None:
						distance[vertex] = distance[coordinate] + 1
						# increase the distance of the vertex by the coordinate+1
						queue.append(vertex)
						# update the list of parent nodes in the dictionary
						parent[vertex] = coordinate

	path = []
	n = goal_position
	# loop through the grid from the goal position and update the shortest path
	while n is not None:
    		# insert the shortest path into the return path
			path.insert(0,n)
			# set the next node to the parent of the previous inserted node
			n = parent[n]
	return path, nodes_expanded

if __name__ == "__main__":
	files = ["part1/mediumMaze.txt", "part1/bigMaze.txt", "part1/openMaze.txt"]

	for file in files:
		# pull the required files and information for bfs from utils.py
		grid, graph, pacman_position, goal_positions = utils.load_puzzle(file)
		path, nodes_expanded = bfs(graph, pacman_position, goal_positions[0])
		# print out graph solution, path cost, and number of expanded nodes
		utils.draw_solution_to_grid(grid, path)
		utils.print_grid(grid)
		print("path cost is  : ", len(path)-1)
		print("nodes expanded: ", nodes_expanded)
		print()
