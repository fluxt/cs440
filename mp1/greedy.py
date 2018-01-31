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

print(goal_positions)
