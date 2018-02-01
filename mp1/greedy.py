import numpy as np
import heapq
import utils

def heuristics(pos1, pos2):
	return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[0])

def gbfs(graph, pacman_position, goal_positions):
	goal = goal_positions[0]
	prev = {}
	visited = {pos: False for pos in graph}
	visited[pacman_position] = True
	hq = []
	heapq.heappush(hq, (heuristics(pacman_position, goal), pacman_position))
	while hq:
		dist, min_node = heapq.heappop(hq)
		if min_node == goal:
			break
		for next_node in graph[min_node]:
			if visited[next_node] == False:
				visited[next_node] = True
				heapq.heappush(hq, (heuristics(next_node, goal), next_node))
				prev[next_node] = min_node

	path = []
	current = goal
	while current in prev:
		path.append(current)
		current = prev[current]
	path.append(pacman_position)

	# print(list(visited.values()).count(True))
	# print(path)
	# print(len(path))

	path.reverse()
	return path

if __name__ == "__main__":
	grid, graph, pacman_position, goal_positions = utils.load_puzzle("part1/mediumMaze.txt")
	
	path = gbfs(graph, pacman_position, goal_positions)

	utils.draw_solution_to_grid(grid, path)
	utils.print_grid(grid)
