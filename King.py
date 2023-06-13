import pygame

from Piece import Piece


class King(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		images_path = 'images/' + color[0] + 'K.png'
		self.images = pygame.image.load(images_path)
		self.images = pygame.transform.scale(self.images, (board.square_width - 20, board.square_height - 20))

		self.notation = 'K' #обозначение

	def get_possible_moves(self, board):
		output = []
		moves = [
			(0, -1), # north
			(1, -1), # northeast
			(1, 0), # east
			(1, 1), # southeast
			(0, 1), # south
			(-1, 1), # southwest
			(-1, 0), # west
			(-1, -1), # northwest
		]
		for move in moves: #движение
			new_pos = (self.x + move[0], self.y + move[1])
			if (new_pos[0] < 8 and new_pos[0] >= 0 and new_pos[1] < 8 and new_pos[1] >= 0):
				output.append([board.get_playing_from_pos(new_pos)])
		return output

	def location_in_the_side(self, board):
		if not self.has_moved:

			if self.color == 'white':
				queen_rook = board.get_piece_from_pos((0, 7))
				king_rook = board.get_piece_from_pos((7, 7))
				if queen_rook != None:
					if not queen_rook.has_moved:
						if [board.get_piece_from_pos((i, 7)) for i in range(1, 4)] == [None, None, None]:
							return 'queen'
				if king_rook != None:
					if not king_rook.has_moved:
						if [board.get_piece_from_pos((i, 7)) for i in range(5, 7)] == [None, None]:
							return 'king'

			elif self.color == 'black':
				queen_rook = board.get_piece_from_pos((0, 0))
				king_rook = board.get_piece_from_pos((7, 0))
				if queen_rook != None:
					if not queen_rook.has_moved:
						if [board.get_piece_from_pos((i, 0)) for i in range(1, 4)] == [None, None, None]:
							return 'queen'
				if king_rook != None:
					if not king_rook.has_moved:
						if [board.get_piece_from_pos((i, 0)) for i in range(5, 7)] == [None, None]:
							return 'king'

	def allowed_moves(self, board):
		output = []
		for playing in self.possible_moves(board):
			if not board.in_check(self.color, board_change=[self.pos, playing.pos]):
				output.append(playing)
		if self.location_in_the_side(board) == 'queen':
			output.append(board.get_playing_from_pos((self.x - 2, self.y)))
		if self.location_in_the_side(board) == 'king':
			output.append(board.get_playing_from_pos((self.x + 2, self.y)))
		return output
