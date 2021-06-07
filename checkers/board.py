from copy import deepcopy
from functools import reduce
from board_searcher import BoardSearcher
from board_initializer import BoardInitializer

class Board:
	"""

	checkers board
	has a list of pieces with their positions,
	current player,
	size of board.
	gets list of possible moves, moves pieces, changes players after each turn
	new board created for each move

	"""
	def __init__(self):
		""" initialize board object. set player id to 1, set size and number of pieces to standard checkers setup"""
		self.player_turn = 1
		self.width = 4
		self.height = 8
		self.position_count = self.width * self.height
		self.rows_per_user_with_pieces = 3
		self.position_layout = {}
		self.piece_requiring_further_capture_moves = None
		self.previous_move_was_capture = False
		self.searcher = BoardSearcher()
		BoardInitializer(self).initialize()

	def count_movable_player_pieces(self, player_number = 1):
		""" return the number of movable pieces for the current player """
		return reduce((lambda count, piece: count + (1 if piece.is_movable() else 0)), self.searcher.get_pieces_by_player(player_number), 0)

	def get_possible_moves(self):
		""" if there are availble capture moves for the current player, return list of capture moves, otherwise return list of possible positional moves """
		capture_moves = self.get_possible_capture_moves()
		if capture_moves: return capture_moves
		else: return self.get_possible_positional_moves()

	def get_possible_capture_moves(self):
		""" return list of possible capture moves for all of a player' pieces """
		return reduce((lambda moves, piece: moves + piece.get_possible_capture_moves()), self.searcher.get_pieces_in_play(), [])

	def get_possible_positional_moves(self):
		""" return list of possible capture moves for all of a player' pieces """
		return reduce((lambda moves, piece: moves + piece.get_possible_positional_moves()), self.searcher.get_pieces_in_play(), [])

	def position_is_open(self, position):
		""" call board searcher function to see if a piece is at a given position.  return true if not """
		return not self.searcher.get_piece_by_position(position)

	def create_new_board_from_move(self, move):
		""" create a new board with changed piece positions based on a given move """
		new_board = deepcopy(self)

		if move in self.get_possible_capture_moves():
			new_board.perform_capture_move(move)
		else:
			new_board.perform_positional_move(move)

		return new_board

	def perform_capture_move(self, move):
		""" 
		move current player piece over enemy piece
		call capture method on enemy piece
		update possible capture moves list
		capture again if possible
		switch turns

		"""
		self.previous_move_was_capture = True
		piece = self.searcher.get_piece_by_position(move[0])
		originally_was_king = piece.king
		enemy_piece = piece.capture_move_enemies[move[1]]
		enemy_piece.capture()
		self.move_piece(move)
		further_capture_moves_for_piece = [capture_move for capture_move in self.get_possible_capture_moves() if move[1] == capture_move[0]]

		if further_capture_moves_for_piece and (originally_was_king == piece.king):
			self.piece_requiring_further_capture_moves = self.searcher.get_piece_by_position(move[1])
		else:
			self.piece_requiring_further_capture_moves = None
			self.switch_turn()

	def perform_positional_move(self, move):
		""" move piece to new position and switch turns """
		self.previous_move_was_capture = False
		self.move_piece(move)
		self.switch_turn()

	def switch_turn(self):
		""" switch player from 1 to 2 or from 2 to 1 """
		if self.player_turn == 2: self.player_turn = 1 
		else: self.player_turn = 2

	def move_piece(self, move):
		""" change board piece list to change the position of a piece in the list """
		self.searcher.get_piece_by_position(move[0]).move(move[1])
		self.pieces = sorted(self.pieces, key = lambda piece: piece.position if piece.position else 0)

	def is_valid_row_and_column(self, row, column):
		""" check that a given row,column pair is within the bounds of the board """
		if row < 0 or row >= self.height:
			return False

		if column < 0 or column >= self.width:
			return False

		return True

	def __setattr__(self, name, value):
		""" reset each piece for a new board, build board with board searcher """
		super(Board, self).__setattr__(name, value)

		if name == 'pieces':
			[piece.reset_for_new_board() for piece in self.pieces]

			self.searcher.build(self)