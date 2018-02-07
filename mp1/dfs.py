import numpy as np
import utils
from collections import defaultdict

def dfs(graph, pacman_pos, goal_position):
	distance = {node:None for node in graph}
	#distance dict
	distance[pacman_pos] = 0
    # predecessors dict
	parent = defaultdict(lambda: None)
	stack = [pacman_pos]
	nodes_expanded = 0
	#iterate through the stack and check each object in the graph
	while stack:
			coordinate = stack.pop()
			nodes_expanded += 1
			if coordinate == goal_position:
				break
			for vertex in graph[coordinate]:
				if distance[vertex] is None:
						distance[vertex] = distance[coordinate] + 1
						stack.append(vertex)
						parent[vertex] = coordinate

    # retrieve shortest path
	path = []
	n = goal_position
	while n is not None:
			path.insert(0,n)
			n = parent[n]
	print (path)
	print(goal_position)
	return path, nodes_expanded

if __name__ == "__main__":
	grid, graph, pacman_pos, goal_positions = utils.load_puzzle("part1/mediumMaze.txt")
	path, nodes_expanded = dfs(graph, pacman_pos, goal_positions[0])
	print(nodes_expanded)
	print(len(path)-1)
	utils.draw_solution_to_grid(grid, path)
	utils.print_grid(grid)
# path = dfs(graph, pacman_pos, goal_positions[0])
# print(path)
# for pos in path[1:]:
# 	grid[pos] = '.'
#
# for row in grid.T:
# 	print(''.join(row))
