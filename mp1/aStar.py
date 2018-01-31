import numpy as np

import fileinput

grid = np.array([[c for c in line if (c != '\n' and c != '\r')] for line in fileinput.input()]).T

width, height = grid.shape

graph = {(x, y): [] for x in range(width) for y in range(height) if grid[x][y] != '%'}

for (x, y) in graph:
	if (x+1) < width and grid[x+1, y] != '%':
		graph[(x, y)].append((x+1, y)) #right
	if (x-1) >= 0 and grid[x-1, y] != '%':
		graph[(x, y)].append((x-1, y)) #left
	if (y+1) < height and grid[x, y+1] != '%':
		graph[(x, y)].append((x, y+1)) #down
	if (y-1) >= 0 and grid[x, y-1] != '%':
		graph[(x, y)].append((x, y-1)) # up

pacman_pos = np.where(grid == 'P')
pacman_pos = (pacman_pos[0][0], pacman_pos[1][0])

goal_positions = np.where(grid == '.')
goal_positions = [(goal_positions[0][n], goal_positions[1][n]) for n in range(len(goal_positions[0]))]


def heuristic_cost_estimate(pos):
	return abs(pos[0] - goal_positions[0][0]) + abs(pos[1] - goal_positions[0][1])

closed_set = set()
open_set = {pacman_pos}
came_from = dict()

g_score = {pos : float("inf") for pos in graph}
g_score[pacman_pos] = 0

f_score = {pos : float("inf") for pos in graph}

path = []

while(open_set):
	current = min(open_set, key= lambda x : f_score[x])
	if (current == goal_positions[0]):
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
			f_score[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor)

while current in came_from:
	current = came_from[current]
	path.append(current)
print(path)
print(len(path))

for pos in path[:-1]:
	grid[pos] = '.'

for row in grid.T:
	print(''.join(row))
