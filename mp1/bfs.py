import numpy as np
import fileinput
import utils

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

def bfs(pacman_pos, goal_positions, graph):
#print(goal_positions)
	explored = []
	queue = [[pacman_pos]]

	while queue:
#	if pacman_pos == goal_positions[0]:
	#	break;
		path = queue.pop(0)
		node = path[-1]
		if node not in explored:
			neighbours = graph[node]
			explored.append(node)
			for neighbour in neighbours:
				new_path = list(path)
				new_path.append(neighbour)
				queue.append(new_path)
				if neighbour == goal_positions:
					return new_path
	return path

new_path = bfs(pacman_pos, goal_positions[0], graph)
print(new_path)
print(len(new_path))

for pos in new_path[1:]:
	grid[pos] = '.'

for row in grid.T:
	print(''.join(row))
