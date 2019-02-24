"""
Given points on a plane, find the 2 closest points
"""

# import random

# xs = [random.randint(1,100) for i in range(50)]
# ys = [random.randint(1,100) for i in range(50)]

# points = list(zip(xs,ys))

# print (points)


import math



myPoints = [(46, 98), (6, 19), (28, 61), (49, 83), (87, 28), (3, 70), (21, 9), (73, 66), \
(82, 86), (85, 55), (23, 54), (40, 69), (77, 56), (39, 79), (9, 94), (69, 35), (12, 47), \
(74, 61), (12, 42), (69, 21), (67, 92), (33, 52), (79, 73), (54, 86), (60, 17), (30, 41), \
(79, 30), (48, 79), (79, 16), (51, 88), (59, 100), (54, 16), (40, 17), (64, 42), (71, 8), \
(100, 12), (17, 100), (79, 35), (38, 99), (78, 37), (70, 70), (13, 50), (84, 64), (30, 45), \
(97, 10), (99, 28), (32, 17), (45, 54), (59, 73), (30, 28)]



def closest_points(point_list):

	ax = sorted(point_list, key = lambda i: i[0])
	ay = sorted(point_list, key = lambda i: i[1])



	def closest_points_rec(ax, ay):

		ln_ax = len(ax)


		if ln_ax <= 3:
			return brute(ax)

		mid = ln_ax // 2

		Lx = ax[:mid]
		Rx = ax[mid:]

		midpoint_x = ax[mid][0]

		Ly = []
		Ry = []

		for point in ax:
			if point[0] <= midpoint_x:
				Ly.append(point)
			else:
				Ry.append(point)


		(p1, q1, min1) = closest_points_rec(Lx, Ly)

		(p2, q2, min2) = closest_points_rec(Rx, Ry)

		if min1 <= min2:
			d = min1
			min_pair = (p1,q1)

		else:
			d = min2
			min_pair = (p2,q2)


		(p3, q3, min3) = closest_split_pair(ax,ay,d, min_pair)

		if d <= min3:
			return min_pair[0], min_pair[1], d
		else:
			return p3, q3, min3

	def dist(p1, p2):
		return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

	def brute(ax):
		mi = dist(ax[0], ax[1])
		p1 = ax[0]
		p2 = ax[1]
		ln_ax = len(ax)
		if ln_ax == 2:
			return p1, p2, mi
		for i in range(ln_ax-1):
			for j in range(i + 1, ln_ax):
				if i != 0 and j != 1:
					d = dist(ax[i], ax[j])
					if d < mi:  # Update min_dist and points
						mi = d
						p1, p2 = ax[i], ax[j]
		return p1, p2, mi

	def closest_split_pair(p_x, p_y, delta, best_pair):
		ln_x = len(p_x)  # store length - quicker
		mx_x = p_x[ln_x // 2][0]  # select midpoint on x-sorted array
		# Create a subarray of points not further than delta from
		# midpoint on x-sorted array
		s_y = [x for x in p_y if mx_x - delta <= x[0] <= mx_x + delta]
		best = delta  # assign best value to delta
		ln_y = len(s_y)  # store length of subarray for quickness
		for i in range(ln_y - 1):
			for j in range(i+1, min(i + 7, ln_y)):
				p, q = s_y[i], s_y[j]
				dst = dist(p, q)
				if dst < best:
					best_pair = p, q
					best = dst
		return best_pair[0], best_pair[1], best


	return closest_points_rec(ax,ay)



print (closest_points(myPoints))
