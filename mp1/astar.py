import numpy as np
import utils


def heuristic_cost_estimate(pos, goal_position):
	return  abs(pos[0] - goal_position[0]) + abs(pos[1] - goal_position[1])

def a_star(graph, pacman_pos, goal_position):
	closed_set = set()
	open_set = {pacman_pos}
	came_from = dict()

	g_score = {pos : float("inf") for pos in graph}
	g_score[pacman_pos] = 0

	f_score = {pos : float("inf") for pos in graph}

	path = []

	while(open_set):
		current = min(open_set, key= lambda x : f_score[x])
		if (current == goal_position):
			path.append(current)
			break

		open_set.remove(current)
		closed_set.add(current)

		for neighbor in graph[current]:
			if neighbor in closed_set:
				continue

			if neighbor not in open_set:
				open_set.add(neighbor)

			tentative_g_score = g_score[current] + 1
			if tentative_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = tentative_g_score
				f_score[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor, goal_position)

	while current in came_from:
		current = came_from[current]
		path.append(current)

	path.reverse()
	return path, len(closed_set)

if __name__ == "__main__":
	files = ["part1/mediumMaze.txt", "part1/bigMaze.txt", "part1/openMaze.txt"]
	
	for file in files:
		grid, graph, pacman_position, goal_positions = utils.load_puzzle(file)
		path, nodes_expanded = a_star(graph, pacman_position, goal_positions[0])

		utils.draw_solution_to_grid(grid, path)
		utils.print_grid(grid)
		print("path cost is  : ", len(path)-1)
		print("nodes expanded: ", nodes_expanded)
		print()
