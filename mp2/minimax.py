import numpy as np
import gomoku

class MiniMax:
	def __init__(self, color, max_depth):
		self.color = color
		self.max_depth = max_depth-1 # minus one because the first one is not recursive
		self.nodes_expanded = []
		self.total_nodes = 0

	def get_nodes_expanded(self):
		return self.nodes_expanded

	def reset(self):
		self.nodes_expanded = []

	def check_end(self, game_board):
		return gomoku.get_game_status(game_board)

	def heuristic(self, game_board):
		ret = 0

		# check if game is over
		end_result = gomoku.get_game_status(game_board)
		if end_result == 3:
			return 0
		elif end_result == 1:
			return 10000
		elif end_result == 2:
			return -10000

		# if four in a row with unblocked ends exist, give 500 points
		if gomoku.has_pattern_position(game_board, [0, 1, 1, 1, 1, 0]):
			ret += 1000

		if gomoku.has_pattern_position(game_board, [0, 2, 2, 2, 2, 0]):
			ret -= 1000

		# if three in a row with unblocked ends exist, give 100 points
		if gomoku.has_pattern_position(game_board, [0, 1, 1, 1, 0]):
			ret += 100

		if gomoku.has_pattern_position(game_board, [0, 2, 2, 2, 0]):
			ret -= 100

		# if three in a row with unblocked ends exist, give 100 points
		if gomoku.has_pattern_position(game_board, [0, 1, 1, 0, 1, 0]):
			ret += 100

		if gomoku.has_pattern_position(game_board, [0, 2, 2, 0, 2, 0]):
			ret -= 100

		# if three in a row with unblocked ends exist, give 100 points
		if gomoku.has_pattern_position(game_board, [0, 1, 0, 1, 1, 0]):
			ret += 100

		if gomoku.has_pattern_position(game_board, [0, 2, 0, 2, 2, 0]):
			ret -= 100

		# incentivize center positions over edges
		for i in range(7):
			for j in range(7):
				if game_board[i][j] == 1:
					ret += 3-max(abs(i-3), abs(j-3))
				elif game_board[i][j] == 2:
					ret -= 3-max(abs(i-3), abs(j-3))

		return ret

	def getMove(self, game_board_original):
		game_board = game_board_original.copy() # make a copy
		
		self.total_nodes = 1 # the getMove node is the node expanded

		# list of all possible moves
		empty_squares = [tuple(e) for e in np.argwhere(game_board==0)]
		if self.color == 1: # maximizing
			best_value = float("-inf")
			for coord in empty_squares:
				game_board[coord] = 1 # make a move
				value = self.getMoveRecursive(game_board, self.max_depth, 2)
				if value > best_value:
					best_value = value
					best_coord = coord
				game_board[coord] = 0 # backtrack
		else: # minimizing
			best_value = float("inf")
			for coord in empty_squares:
				game_board[coord] = 2 # make a move
				value = self.getMoveRecursive(game_board, self.max_depth, 1)
				if value < best_value:
					best_value = value
					best_coord = coord
				game_board[coord] = 0 # backtrack
		
		self.nodes_expanded.append(self.total_nodes) # keep track of all nodes expanded
		return best_coord # return coordinate with the best score

	def getMoveRecursive(self, game_board, depth, color):
		if depth == 0 or self.check_end(game_board) != 0:
			return self.heuristic(game_board)

		self.total_nodes += 1

		empty_squares = [tuple(e) for e in np.argwhere(game_board==0)]
		if color == 1: # maximizing
			best_value = float("-inf")
			for coord in empty_squares:
				game_board[coord] = 1 # make a move
				best_value = max(best_value, self.getMoveRecursive(game_board, depth-1, 2))
				game_board[coord] = 0 # backtrack
		else: # minimizing
			best_value = float("inf")
			for coord in empty_squares:
				game_board[coord] = 2 # make a move
				best_value = min(best_value, self.getMoveRecursive(game_board, depth-1, 1))
				game_board[coord] = 0 # backtrack
		return best_value

if __name__ == "__main__":
	agent_red = MiniMax(1, 3)
	agent_blu = MiniMax(2, 3)
	gomoku.play_game(agent_blu, agent_red)
	print(agent_red.get_nodes_expanded())
	agent_red.reset()
	print(agent_blu.get_nodes_expanded())
	agent_blu.reset()