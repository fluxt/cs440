import numpy as np
import utils
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

#print(goal_positions)
#DFS(G, v):
#    setLabel(v, VISITED)
#    for Vertex w in G.adjacent(v):
#        if getLabel(w) == UNEXPLORED:
#            setLabel(v, w, DISCOVERY)
#            DFS(G, w)
#        else if getLabel(v, w) == UNEXPLORED:
#            setLabel(v, w, BACK)
# while loop with stack;

# create labels, stack and
def dfs(graph, pacman_pos, goal_positions):
	explored = []
	stack = [[pacman_pos]]

	while stack:
#	if pacman_pos == goal_positions[0]:
#	break;
		path = stack.pop(0)
		node = path[-1]
		if node not in explored:
			neighbours = graph[node]
			explored.append(node)
			for neighbour in neighbours:
				new_path = list(path)
				new_path.append(neighbour)
				stack.append(new_path)
				if neighbour == goal_positions:
					return new_path
	return path

new_path = dfs(graph, pacman_pos, goal_positions[0])
print(new_path)
print(len(new_path))

for pos in new_path[1:]:
	grid[pos] = '.'

for row in grid.T:
	print(''.join(row))
