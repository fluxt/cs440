import numpy as np
import heapq
import utils

def heuristics(pos1, pos2):
	return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def gbfs(graph, pacman_position, goal_position):
	parent = {pos: None for pos in graph}
	visited = {pos: False for pos in graph}
	visited[pacman_position] = True
	hq = []
	heapq.heappush(hq, (heuristics(pacman_position, goal_position), pacman_position))
	nodes_expanded = 0
	while hq:
		dist, min_node = heapq.heappop(hq)
		nodes_expanded += 1
		if min_node == goal_position:
			break
		for next_node in graph[min_node]:
			if visited[next_node] == False:
				visited[next_node] = True
				heapq.heappush(hq, (heuristics(next_node, goal_position), next_node))
				parent[next_node] = min_node
	path = []
	current = goal_position
	while current is not None:
		path.insert(0, current)
		current = parent[current]
	return path, nodes_expanded

if __name__ == "__main__":
	files = ["part1/mediumMaze.txt", "part1/bigMaze.txt", "part1/openMaze.txt"]
	
	for file in files:
		grid, graph, pacman_position, goal_positions = utils.load_puzzle(file)
		path, nodes_expanded = gbfs(graph, pacman_position, goal_positions[0])

		utils.draw_solution_to_grid(grid, path)
		utils.print_grid(grid)
		print("path cost is  : ", len(path)-1)
		print("nodes expanded: ", nodes_expanded)
		print()
