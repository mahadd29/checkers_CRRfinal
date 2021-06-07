from board import Board

class Game:
	"""

	game of checkers object
	a game has a series of boards, and a new board is created after each turn
	moves are kept track of in a list, and non-capture moves are limited so the game ends eventually
	game calls methods to move pieces, checks limits, and determines winner and end of game

	"""
	def __init__(self):
		""" initialize checkers game object.  create new board and empty list of moves """
		self.board = Board()
		self.moves = []
		self.consecutive_noncapture_move_limit = 40
		self.moves_since_last_capture = 0

	def move(self, move):
		""" 
		
		given a move, check that it is possible. 
		if possible, create board with move result, add move to list of moves, 
		increment non capture move count if it is a non caputure move
		
		"""
		if move not in self.get_possible_moves():
			raise ValueError('The provided move is not possible')

		self.board = self.board.create_new_board_from_move(move)
		self.moves.append(move)
		if self.board.previous_move_was_capture:
			self.moves_since_last_capture = 0
		else: 
			self.moves_since_last_capture = self.moves_since_last_capture + 1

		return self

	def move_limit_reached(self):
		""" return True if game has reached limit for moves since last capture  """
		return self.moves_since_last_capture >= self.consecutive_noncapture_move_limit

	def is_over(self):
		""" return True if move limit is reached or there are no more possible moves.  indicates end of game """
		return self.move_limit_reached() or not self.get_possible_moves()

	def get_winner(self):
		""" 
		
		return player id (1 or 2) of the winning player.  return None if game is a draw or still in progress
		if it is enemy's turn and enemy has no movable pieces, player wins
		
		"""
		if self.whose_turn() == 1 and not self.board.count_movable_player_pieces(1):
			return 2
		elif self.whose_turn() == 2 and not self.board.count_movable_player_pieces(2):
			return 1
		else:
			return None

	def get_possible_moves(self):
		""" call method to return list of possible moves from game's board """
		return self.board.get_possible_moves()

	def whose_turn(self):
		""" call method to get id of player whose turn it is """
		return self.board.player_turn
