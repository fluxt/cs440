import numpy as np

# loads puzzle from file as numpy grid, graph, and passes pacman's position and goal positions
# numpy stores (x, y) == (row, column)
# example:
#   utils.load_puzzle("part1/mediumMaze.txt")
#
def load_puzzle(filename):
	with open(filename) as f:
		grid = np.array([[c for c in line.strip()] for line in f.readlines()])

	x_size, y_size = grid.shape

	graph = {(x, y): [] for y in range(y_size) for x in range(x_size) if grid[x][y] != '%'}
	for (x, y) in graph:
		# right
		if (x+1) < x_size and grid[x+1][y] != '%':
			graph[(x, y)].append((x+1, y))
		# left
		if (x-1) >= 0 and grid[x-1][y] != '%':
			graph[(x, y)].append((x-1, y))
		# down
		if (y+1) < y_size and grid[x][y+1] != '%':
			graph[(x, y)].append((x, y+1))
		# up
		if (y-1) >= 0 and grid[x][y-1] != '%':
			graph[(x, y)].append((x, y-1))

	pacman_position = np.where(grid == 'P')
	pacman_position = (pacman_position[0][0], pacman_position[1][0])

	goal_positions = np.where(grid == '.')
	goal_positions = [(goal_positions[0][n], goal_positions[1][n]) for n in range(len(goal_positions[0]))]

	# print(grid)
	# print(graph)
	# print(pacman_position)
	# print(goal_positions)

	return grid, graph, pacman_position, goal_positions

# prints UNTRANSPOSED grid of characters out to standard stream.
def print_grid(grid):
	for row in grid:
		print(''.join(row))

# prints UNTRANSPOSED grid of characters out to filename.
def print_grid_to_file(grid, filename):
	with open(filename, 'w+') as f:
		for row in grid:
			f.write(''.join(row)+'\n')

def draw_solution_to_grid(grid, path):
	for pos in path[1:]:
		grid[pos] = '.'
