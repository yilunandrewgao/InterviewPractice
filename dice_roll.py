"""
Given n x-sided dice, how many ways are there to roll a total sum of y?
"""

"""
This can be solved using generating functions as explained here: http://mathforum.org/library/drmath/view/52207.html
But I will use a dp approach to double-check the answer
"""


def ways_to_roll(num_dice, total_faces, total_sum):

	memo_dict = {}

	def subproblem(sum_remaining, dice_remaining):

		if dice_remaining == 0 and sum_remaining == 0:
			return 1

		elif sum_remaining < dice_remaining:
			return 0

		elif dice_remaining == 1 and sum_remaining <= total_faces:
			return 1

		elif dice_remaining == 1 and sum_remaining > total_faces:
			return 0

		elif (sum_remaining, dice_remaining) in memo_dict:
			return memo_dict[(sum_remaining, dice_remaining)]

		else:

			num_ways = 0

			for i in range(sum_remaining - total_faces, sum_remaining):
				num_ways += subproblem(i, dice_remaining - 1)

			memo_dict[(sum_remaining, dice_remaining)] = num_ways

			return num_ways


	return subproblem(total_sum, num_dice)


# should be 140
print (ways_to_roll(4, 6, 13))


# should be 831204
print (ways_to_roll(10,6,25))