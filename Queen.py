import pygame
from Piece import Piece


class Queen(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)
		images_path = 'images/' + color[0] + 'Q.png'
		self.images = pygame.image.load(images_path)
		self.images = pygame.transform.scale(self.images, (board.square_width - 20, board.square_height - 20))
		self.notation = 'Q'

	def get_possible_moves(self, board):
		output = []

		moves_north = []
		for y in range(self.y)[::-1]:
			moves_north.append(board.get_playing_from_pos((self.x, y)))
		output.append(moves_north)

		moves_northeast = []
		for i in range(1, 8):
			if self.x + i > 7 or self.y - i < 0:
				break
			moves_northeast.append(board.get_playing_from_pos((self.x + i, self.y - i)))
		output.append(moves_northeast)

		moves_east = []
		for x in range(self.x + 1, 8):
			moves_east.append(board.get_playing_from_pos((x, self.y)))
		output.append(moves_east)

		moves_southeast = []
		for i in range(1, 8):
			if self.x + i > 7 or self.y + i > 7:
				break
			moves_southeast.append(board.get_playing_from_pos((self.x + i, self.y + i)))
		output.append(moves_southeast)

		moves_south = []
		for y in range(self.y + 1, 8):
			moves_south.append(board.get_playing_from_pos((self.x, y)))
		output.append(moves_south)

		moves_southwest = []
		for i in range(1, 8):
			if self.x - i < 0 or self.y + i > 7:
				break
			moves_southwest.append(board.get_playing_from_pos((self.x - i, self.y + i)))
		output.append(moves_southwest)

		moves_west = []
		for x in range(self.x)[::-1]:
			moves_west.append(board.get_playing_from_pos((x, self.y)))
		output.append(moves_west)

		moves_northwest = []
		for i in range(1, 8):
			if self.x - i < 0 or self.y - i < 0:
				break
			moves_northwest.append(board.get_playing_from_pos((self.x - i, self.y - i)))
		output.append(moves_northwest)
		return output

