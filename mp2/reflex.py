import gomoku.py

class ReflexAgent:
	def __init__(self, player_num):
		self.player_num = player_num

	def getMove(self, game_board):
		return get_move(game_board, self.player_num)

def get_four_block_move(board, player_num):


def get_move(board, player_num):
	# 1. check for winning with just one more stone
	# TODO: do the left>down>right>up thing
	for x in range(7):
		for y in range(7):
			if not board[x][y]:
				board[x][y] = player_num
				if get_game_status(board) == player_num:
					return (x, y)
				board[x][y] = 0

	
