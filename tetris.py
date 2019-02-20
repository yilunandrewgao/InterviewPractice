"""
Make a Tetris Game

Code is based on this gist: https://gist.github.com/silvasur/565419 with a few changes
"""


import pygame
import random
import numpy
import sys


# The configuration
CELL_SIZE =	18
COLS =		10
ROWS =		22
MAX_FPS = 	30

COLORS = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(35,  35,  35)]

# Changed the length of the I so that rotation is more correct
class Shape():

	# T, S, Z, J, L, I, O
	TetrisShapes = [
		[[1, 1, 1],
		 [0, 1, 0],
		 [0, 0, 0]],
		
		[[0, 2, 2],
		 [2, 2, 0],
		 [0, 0, 0]],
		
		[[3, 3, 0],
		 [0, 3, 3],
		 [0, 0, 0]],
		
		[[4, 0, 0],
		 [4, 4, 4],
		 [0, 0, 0]],
		
		[[0, 0, 5],
		 [5, 5, 5],
		 [0, 0, 0]],
		
		[[0, 0, 0],
		 [6, 6, 6],
		 [0, 0, 0]],
		
		[[0 ,0, 0],
		 [0, 7, 7],
		 [0, 7, 7]]
	]

	def __init__(self, upperx, uppery, shape_index = None):

		if shape_index is None:
			shape_index = random.randint(0, len(self.TetrisShapes) - 1)

		self.upperx = upperx - len(self.TetrisShapes[shape_index][0]) // 2
		self.uppery = uppery

		self.matrix = numpy.array(self.TetrisShapes[shape_index])

		(self.height, self.width) = numpy.shape(self.matrix)

	# rotate clockwise 90 deg around (1, 1)
	def rotate_counterclockwise(self):
		self.matrix = numpy.rot90(self.matrix)

	def drop(self):
		self.uppery += 1

	def moveto(self, new_x):

		self.upperx = new_x


class Board():

	def __init__(self, width, height):

		self.width = width
		self.height = height
		self.matrix = numpy.zeros((height, width), dtype = int)

	def clear_row(self, row_index):

		if not (0 in self.matrix[row_index, :]):
			self.matrix = numpy.delete(self.matrix, row_index, axis = 0)
			# add a empty row at the top
			self.matrix = numpy.insert(self.matrix, 0, 0, axis = 0)

	def check_rows(self):

		for row_index in range(self.height):
			self.clear_row(row_index)

	def new_board(self):
		self.matrix = numpy.zeros((height, width), dtype = int)


class TetrisApp():

	def __init__(self):

		pygame.init()
		pygame.key.set_repeat(250,25)
		self.width = CELL_SIZE * COLS
		self.height = CELL_SIZE * ROWS
		self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in range(COLS)] for y in range(ROWS)]

		self.default_font =  pygame.font.Font(
			pygame.font.get_default_font(), 12)

		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.event.set_blocked(pygame.MOUSEMOTION)

		self.gameover = False
		self.paused = False

		self.next_stone = Shape(COLS // 2 , 0)
		self.init_game()

	def check_collision(self):

		for x in range(self.stone.width):
			for y in range(self.stone.height):
				try:
					if self.stone.matrix[y,x] and self.board.matrix[y+self.stone.uppery, x + self.stone.upperx]:
						return True
				except IndexError:
					return True
		return False

	def merge_stone(self):

		for x in range(self.stone.width):
			for y in range(self.stone.height):
				try:
					if not self.board.matrix[y+self.stone.uppery, x + self.stone.upperx]:
						self.board.matrix[y+self.stone.uppery, x + self.stone.upperx] = self.stone.matrix[y,x]
				except:
					pass

	def new_stone(self):
		self.stone = self.next_stone
		self.next_stone = Shape(COLS // 2, 0)

		if self.check_collision():
			self.gameover = True

	def init_game(self):
		self.board = Board(COLS, ROWS)
		self.new_stone()

		self.gameover = False
		self.paused = False

		pygame.time.set_timer(pygame.USEREVENT, 1000)


	def move(self, delta_x):

		if not self.gameover and not self.paused:
			new_x = self.stone.upperx + delta_x

			if new_x < 0:
				new_x = 0

			if new_x > COLS - self.stone.width:
				new_x = COLS - self.stone.width

			if not self.check_collision():
				self.stone.moveto(new_x)

	def quit(self):
		sys.exit()

	def drop(self):

		if not self.gameover and not self.paused:
			self.stone.uppery += 1

			if self.check_collision():
				self.stone.uppery -= 1
				self.merge_stone()

				self.new_stone()

				self.board.check_rows()

	def toggle_pause(self):
		self.paused = not self.paused

	def start_game(self):
		if self.gameover:
			self.init_game()

	def draw(self):
		#draw the background
		for x in range(COLS):
			for y in range(ROWS):

				val = self.bground_grid[y][x]
				if val:
					pygame.draw.rect(
						self.screen,
						COLORS[val],
						pygame.Rect(
							(x) * CELL_SIZE,
							(y) * CELL_SIZE, 
							CELL_SIZE,
							CELL_SIZE),0)


		# draw the board
		for x in range(self.board.width):
			for y in range(self.board.height):

				val = self.board.matrix[y,x]
				if val:
					pygame.draw.rect(
						self.screen,
						COLORS[val],
						pygame.Rect(
							(x) * CELL_SIZE,
							(y) * CELL_SIZE, 
							CELL_SIZE,
							CELL_SIZE),0)

		# draw the stone
		off_x, off_y  = self.stone.upperx, self.stone.uppery

		for x in range(self.stone.width):
			for y in range(self.stone.height):

				val = self.stone.matrix[y,x]
				if val:
					pygame.draw.rect(
						self.screen,
						COLORS[val],
						pygame.Rect(
							(x + off_x) * CELL_SIZE,
							(y + off_y) * CELL_SIZE, 
							CELL_SIZE,
							CELL_SIZE),0)

	def run(self):


		key_actions = {
			'ESCAPE':	self.quit,
			'LEFT':		lambda:self.move(-1),
			'RIGHT':	lambda:self.move(+1),
			'DOWN':		lambda:self.drop(),
			'p':		self.toggle_pause,
			'SPACE':	self.start_game
		}

		while True:
			self.screen.fill((0,0,0))

			if self.gameover:
				pass
			else:
				pygame.draw.line(self.screen,
					(255,255,255),
					(self.width + 1, 0),
					(self.width + 1, self.height - 1))

				self.draw()
			pygame.display.update()

			for event in pygame.event.get():
				
				if event.type == pygame.USEREVENT:
					self.drop()
				elif event.type == pygame.QUIT:
					self.quit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						self.stone.rotate_counterclockwise()
					else:
						for key in key_actions:
							if event.key == eval("pygame.K_"
							+key):
								key_actions[key]()
					
if __name__ == "__main__":
	App = TetrisApp()
	App.run()

















