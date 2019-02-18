import sys

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
		while index < 0 or index >= len(self.board.array):
			print ("Invalid square")
			index = get_index()

		return index

	def start_game(self):
		while self.board.check_win_con() == (False, False):
			print (self.board)
			index = self.ask_for_input()
			if self.playersTurn == 0:
				self.board.mark_square_x(index)
			else:
				self.board.mark_square_o(index)
			self.playersTurn = (self.playersTurn + 1) % 2


		print (self.board)
		if self.board.check_win_con()[0] == True:
			print ("player0 won")
		else:
			print ("player1 won")





def main():

	myboard = Board()

	mygame = Game(myboard)

	mygame.start_game()
	sys.exit()


if __name__ == "__main__":
	main()





