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

import sys
import heapq

goal = goal_positions[0]
prev = {}
visited = {pos: False for pos in graph}

def gbfs():
  visited[pacman_pos] = True
  hq = []
  heapq.heappush(hq, (heuristics(pacman_pos, goal), pacman_pos))
  while hq:
    dist, min_node = heapq.heappop(hq)
    if min_node == goal:
      break
    for next_node in graph[min_node]:
      if visited[next_node] == False:
        visited[next_node] = True
        heapq.heappush(hq, (heuristics(next_node, goal), next_node))
        prev[next_node] = min_node

def heuristics(pos1, pos2):
  return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[0])

gbfs()

path = []
current = goal
while current in prev:
  current = prev[current]
  path.append(current)
print(path)
print(len(path))

for pos in path[:-1]:
  grid[pos] = '.'

for row in grid.T:
  print(''.join(row))
