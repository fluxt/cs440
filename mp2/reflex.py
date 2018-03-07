import gomoku.py

class ReflexAgent:
	def __init__(self, player_num):
		self.player_num = player_num

	def getMove(self, game_board):
		return get_move(game_board, self.player_num)

def get_four_and_blank_position(board, player_num):
	pos1 = get_pattern_position(board, [0, player_num, player_num, player_num, player_num])
	if (pos1):
		return pos1[0]

	pos2 =  get_pattern_position(board, [player_num, player_num, player_num, player_num, 0])
	if (pos2):
		return pos2[1]

	return 0

def get_move(board, player_num):
	other_player_num = 1 if player_num == 2 else 2

	winning_position = get_four_and_blank_position(board, player_num)
	if winning_position:
		return winning_position

	blocking_position_1 = get_four_and_blank_position(board, player_num)
	if blocking_position_1:
		return blocking_position_1

	three_block = get_pattern_position(board, [0,  player_num, player_num, player_num, 0])
	if three_block:
		return three_block[0]

	
