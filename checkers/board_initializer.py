from .piece import Piece

class BoardInitializer:
	""" initialize a game board with a size, list of positions, and pieces in starting positions """
	def __init__(self, board):
		""" initialize initializer object with a given board """
		self.board = board

	def initialize(self):
		""" call method to build list of positions and place pieces """
		self.build_position_layout()
		self.set_starting_pieces()

	def build_position_layout(self):
		""" create and populate a dictionary of row dictionaries. populate each row with a list of position index numbers"""
		self.board.position_layout = {}
		position = 1

		for row in range(self.board.height):
			self.board.position_layout[row] = {}

			for column in range(self.board.width):
				self.board.position_layout[row][column] = position
				position += 1

	def set_starting_pieces(self):
		""" set list of pieces to starting positions """
		pieces = []
		starting_piece_count = self.board.width * self.board.rows_per_user_with_pieces
		player_starting_positions = {
			1: list(range(1, starting_piece_count + 1)),
			2: list(range(self.board.position_count - starting_piece_count + 1, self.board.position_count + 1))
		}

		for key, row in self.board.position_layout.items():
			for key, position in row.items():
				player_number = 1 if position in player_starting_positions[1] else 2 if position in player_starting_positions[2] else None

				if (player_number):
					pieces.append(self.create_piece(player_number, position))

		self.board.pieces = pieces

	def create_piece(self, player_number, position):
		""" create a piece object with a given player number and position """
		piece = Piece()
		piece.player = player_number
		piece.position = position
		piece.board = self.board

		return piece