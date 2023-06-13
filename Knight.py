import pygame

from Piece import Piece


class Knight(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		images_path = 'images/' + color[0] + 'N.png'
		self.images = pygame.image.load(images_path)
		self.images = pygame.transform.scale(self.images, (board.square_width - 20, board.square_height - 20))

		self.notation = 'N'

	def get_possible_moves(self, board):
		output = []
		moves = [
			(1, -2),
			(2, -1),
			(2, 1),
			(1, 2),
			(-1, 2),
			(-2, 1),
			(-2, -1),
			(-1, -2)
		]

		for move in moves:
			new_pos = (self.x + move[0], self.y + move[1])
			if (new_pos[0] < 8 and new_pos[0] >= 0 and new_pos[1] < 8 and new_pos[1] >= 0):
				output.append([board.get_playing_from_pos(new_pos)])

		return output
