import numpy as np
import utils
from collections import defaultdict


def bfs(graph, pacman_pos, goal_position):
	distance = {node:None for node in graph}
	#distance dict
	distance[pacman_pos] = 0
    # predecessors dict
	parent = defaultdict(lambda: None)
	queue = [pacman_pos]
	nodes_expanded = 0
	while queue:
			coordinate = queue.pop(0)
			nodes_expanded += 1
			if coordinate == goal_position:
				break
			for vertex in graph[coordinate]:
				if distance[vertex] is None:
						distance[vertex] = distance[coordinate] + 1
						queue.append(vertex)
						parent[vertex] = coordinate

    # retrieve shortest path
	path = []
	n = goal_position
	while n is not None:
			path.insert(0,n)
			n = parent[n]
	return path, nodes_expanded

if __name__ == "__main__":
	files = ["part1/mediumMaze.txt", "part1/bigMaze.txt", "part1/openMaze.txt"]
	
	for file in files:
		grid, graph, pacman_position, goal_positions = utils.load_puzzle(file)
		path, nodes_expanded = bfs(graph, pacman_position, goal_positions[0])

		utils.draw_solution_to_grid(grid, path)
		utils.print_grid(grid)
		print("path cost is  : ", len(path)-1)
		print("nodes expanded: ", nodes_expanded)
		print()
