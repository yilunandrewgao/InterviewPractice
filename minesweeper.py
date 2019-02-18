import random
import sys


class Square():

	def __init__(self, index, board_width):

		self.revealed = False
		self.index = index
		self.x = index % board_width
		self.y = index // board_width
		self.adjacent_mines = 0
		self.is_mine = False

	def __repr__(self):

		if self.revealed:
			if self.is_mine:
				return "M"

			else:
				return str(self.adjacent_mines)

		else:
			return " "

	def get_coords(self):
		return (self.x, self.y)

class Board():

	def coords_to_index(self,x,y):

		return y * self.width + x

	def __init__(self, height, width, mines):

		self.height = height
		self.width = width
		self.mines = mines
		self.squares_revealed = 0

		if self.mines > self.height * self.width:
			raise Exception("Too many mines")

		self.array = [Square(i, self.width) for i in range(self.height * self.width)]

		# fill in mines

		random_mine_indices = random.sample(range(self.height * self.width), self.mines)

		# set the mines
		for index in random_mine_indices:
			mysquare = self.array[index]
			mysquare.is_mine = True
			(x,y) = mysquare.get_coords()

			# increment adjacent squares mine count
			if y > 0:
				square_above = self.array[self.coords_to_index(x,y-1)]
				square_above.adjacent_mines += 1
			if y < self.height - 1:
				square_below = self.array[self.coords_to_index(x,y+1)]
				square_below.adjacent_mines += 1
			if x > 0:
				square_left = self.array[self.coords_to_index(x-1,y)]
				square_left.adjacent_mines += 1
			if x < self.width - 1:
				square_right = self.array[self.coords_to_index(x+1,y)]
				square_right.adjacent_mines += 1
			if y > 0 and x > 0:
				square_upperleft = self.array[self.coords_to_index(x-1,y-1)]
				square_upperleft.adjacent_mines += 1
			if y > 0 and x < self.width - 1:
				square_upperright = self.array[self.coords_to_index(x+1,y-1)]
				square_upperright.adjacent_mines += 1
			if y < self.height - 1 and x > 0:
				square_lowerleft = self.array[self.coords_to_index(x-1,y+1)]
				square_lowerleft.adjacent_mines += 1
			if y < self.height - 1 and x < self.width - 1:
				square_lowerright = self.array[self.coords_to_index(x+1,y+1)]
				square_lowerright.adjacent_mines += 1

	def __repr__(self):

		board_to_print = "-"*2*self.width + "\n"

		for y in range(self.height):

			for x in range(self.width):

				board_to_print += self.array[self.coords_to_index(x,y)].__repr__() + "|"

			board_to_print += "\n"+"-"*2*self.width+"\n"

		return board_to_print

	def check_wincon(self):
		if self.height*self.width - self.squares_revealed == self.mines:
			return True
		else: 
			return False

	#returns (game_is_over, game_is_won) or None if square is already revealed
	def reveal_square(self, x, y):

		index = self.coords_to_index(x,y)

		mysquare = self.array[index]

		if mysquare.revealed:
			return
		else:

			mysquare.revealed = True
			self.squares_revealed += 1

			if mysquare.is_mine:
				return (True,False)
			else:
				# check wincon
				if self.check_wincon():
					return (True, True)

				else:

					# recursively reveal squares if current square has 0 adjacent mines

					if mysquare.adjacent_mines == 0:
						# recursively reveal adjacent squares
						if y > 0:
							self.reveal_square(x, y-1)
						if y < self.height - 1:
							self.reveal_square(x, y+1)
						if x > 0:
							self.reveal_square(x-1, y)
						if x < self.width - 1:
							self.reveal_square(x+1, y)
						if y > 0 and x > 0:
							self.reveal_square(x-1, y-1)
						if y > 0 and x < self.width - 1:
							self.reveal_square(x+1, y-1)
						if y < self.height - 1 and x > 0:
							self.reveal_square(x-1, y+1)
						if y < self.height - 1 and x < self.width - 1:
							self.reveal_square(x+1, y+1)


					if self.check_wincon():
						return (True, True)

					else:
						return (False, False)

			

				

class Game():

	def __init__(self, board):

		self.board = board
		self.game_over = False
		self.won = False
		self.turn = 0

	def click_square(self, x, y):

		result = self.board.reveal_square(x,y)

		if result:
			(self.game_over, self.won) = result
			return result
		else:
			return

		

	def start_game(self):

		while not self.game_over:
			print (self.board)

			(x,y) = self.ask_for_input()
			result = self.click_square(x,y)

			if result != None:
				(self.game_over, self.won) = result
			else:
				print ("This square has already been revealed")

		if self.won:
			print (self.board)
			print ("You won")
		else:
			print (self.board)
			print ("You lost")
		

	def ask_for_input(self):

		def get_coords():
			x = int(input("enter the x coordinate: "))
			y = int(input("enter the y coordinate: "))

			return (x,y)

		(x,y) = get_coords()

		while x < 0 or x > self.board.width-1 or y < 0 or y > self.board.height-1:
			print ("invalid coordinates")
			(x,y) = get_coords()

		return (x,y)







def main():

	myboard = Board(10,10,20)
	mygame = Game(myboard)

	mygame.start_game()
	sys.exit()


if __name__ == "__main__":
	main()

