import fileinput

grid = [[c for c in line if (c != '\n' and c != '\r')] for line in fileinput.input()]
print(grid)
