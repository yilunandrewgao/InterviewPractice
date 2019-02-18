"""
implement TicTacToe
"""

import sys
import random

class Square():

	def __init__(self, index):
		self.value = None
		self.index = index

	def __repr__(self):
		if self.value == None:
			return " "
		else:
			return self.value


"""
0 1 2
3 4 5
6 7 8
"""
class Board():

	def __init__(self):

		self.array = [Square(i) for i in range(9)]

	def mark_square_x(self,index):
		self.array[index].value = 'X'


	def mark_square_o(self, index):
		self.array[index].value = 'O'

	def check_win_con(self):
		winning_combos = [set([0,1,2]), set([3,4,5]), set([6,7,8]), set([0,3,6]), set([1,4,7]), set([2,5,8]), set([0,4,8]), set([2,4,6])]

		all_x_indices = set([index for index, square in enumerate(self.array) if square.value == 'X'])
		all_o_indices = set([index for index, square in enumerate(self.array) if square.value == 'O'])

		x_win = False
		o_win = False

		for combo in winning_combos:
			if all_x_indices >= combo:
				x_win = True
			if all_o_indices >= combo:
				o_win = True

		return (x_win, o_win)

	def check_tie(self):
		all_empty_indices = [index for index, square in enumerate(self.array) if square.value == None]

		if len(all_empty_indices) == 0:
			return True
		else:
			return False

	def __repr__(self):

		board_to_print = \
		"-----\n" + \
		self.array[0].__repr__() + "|" + self.array[1].__repr__() + "|" + self.array[2].__repr__() + "\n" + \
		"-----\n" + \
		self.array[3].__repr__() + "|" + self.array[4].__repr__() + "|" + self.array[5].__repr__() + "\n" + \
		"-----\n" + \
		self.array[6].__repr__() + "|" + self.array[7].__repr__() + "|" + self.array[8].__repr__() + "\n" + \
		"-----\n"

		return board_to_print


# player0 is X, player1 is O
class Game():

	def __init__(self, board):

		self.board = board
		self.game_over = False
		self.playersTurn = 0

	def ask_for_input(self):
		print ("It is player" + str(self.playersTurn) + "'s turn.")
		def get_index():
			index = int(input("Which square do you want to mark: "))

			return index

		index = get_index()
		while index < 0 or index >= len(self.board.array) or self.board.array[index].value != None:
			print ("Invalid square")
			index = get_index()

		return index

	def start_game(self):
		while self.board.check_win_con() == (False, False) and self.check_tie() == False:
			print (self.board)
			index = self.ask_for_input()
			if self.playersTurn == 0:
				self.board.mark_square_x(index)
			else:
				self.board.mark_square_o(index)
			self.playersTurn = (self.playersTurn + 1) % 2


		print (self.board)
		if self.board.check_tie():
			print ("Tied Game")
		else:		
			if self.board.check_win_con()[0] == True:
				print ("player0 won")
			else:
				print ("player1 won")

class SinglePlayerGame(Game):

	def __init__(self, board, computer_symbol = 'X'):
		super().__init__(board)

		self.computer_symbol = computer_symbol

		self.mycomputer = Computer(self.board, symbol = self.computer_symbol)

	def start_game(self):
		while self.board.check_win_con() == (False, False) and self.board.check_tie() == False:
			print (self.board)

			if (self.playersTurn == 0 and self.computer_symbol == 'X') or (self.playersTurn == 1 and self.computer_symbol == 'O'):
				self.board.mark_square_x(self.mycomputer.make_move())
			else:
				index = self.ask_for_input()
				self.board.mark_square_o(index)
			self.playersTurn = (self.playersTurn + 1) % 2


		print (self.board)
		if self.board.check_tie():
			print ("Tied Game")
		else:		
			if self.board.check_win_con()[0] == True:
				print ("player0 won")
			else:
				print ("player1 won")

class Computer():

	def __init__(self, board, symbol = 'X'):
		self.board = board
		self.symbol = symbol
		if self.symbol != 'X' and self.symbol != 'O':
			raise Exception("Incorrect Symbol")

	def make_move(self):

		# check if the game is already over 
		if self.board.check_win_con() != (False, False) or self.board.check_tie() == True:
			raise Exception("Game is already over")
		else:
			# get set of opponent's squares
			if self.symbol == 'X':
				opponents_squares = set([index for index, square in enumerate(self.board.array) if square.value == 'O'])
				my_squares = set([index for index, square in enumerate(self.board.array) if square.value == 'X'])
			else:
				opponents_squares = set([index for index, square in enumerate(self.board.array) if square.value == 'X'])
				my_squares = set([index for index, square in enumerate(self.board.array) if square.value == 'O'])

			# if you can win, do it
			winning_combos = [set([0,1,2]), set([3,4,5]), set([6,7,8]), set([0,3,6]), set([1,4,7]), set([2,5,8]), set([0,4,8]), set([2,4,6])]
			for combo in winning_combos:
				for elem in combo:
					almost_complete_combo = combo.copy()
					almost_complete_combo.remove(elem)

					if my_squares >= almost_complete_combo and self.board.array[elem].value == None:
						return elem

			# if your opponent is about to win, block it
			for combo in winning_combos:
				for elem in combo:
					almost_complete_combo = combo.copy()
					almost_complete_combo.remove(elem)

					if opponents_squares >= almost_complete_combo and self.board.array[elem].value == None:
						return elem

			# if middle square is empty, take it
			if self.board.array[4].value == None:
				return 4

			# if a corner is open, take it
			open_corners = [index for index, square in enumerate(self.board.array) if (square.value == None and index in [0,2,6,8])]
			if len(open_corners) > 0:
				return random.choice(open_corners)

			# if an edge is open, take it
			open_edges = [index for index, square in enumerate(self.board.array) if (square.value == None and index in [1,3,5,7])]
			if len(open_edges) > 0:
				return random.choice(open_corners)

			# otherwise, raise exception
			raise Exception("No more empty squares")







def main():

	myboard = Board()

	mygame = SinglePlayerGame(myboard, 'O')

	mygame.start_game()
	sys.exit()


if __name__ == "__main__":
	main()





