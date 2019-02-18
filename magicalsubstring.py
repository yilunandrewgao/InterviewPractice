"""
A magical sub-sequence of a string S is a sub-sequence of S that contains all five vowels in order. 
Find the length of largest magical sub-sequence of a string S.

For example, if S = aeeiooua, then aeiou and aeeioou are magical sub-sequences but aeio and aeeioua are not.
"""


def LIS(magical):

	vowels = ['a','e','i','o','u']

	max_substring_len_ending_with_vowel = [0,0,0,0,0]


	for vowel in magical:

		vowel_num = vowels.index(vowel)
		prev_vowel_num = vowel_num - 1

		if vowel_num == 0:

			max_substring_len_ending_with_vowel[0] += 1

		else:
			 max_substring_len_ending_with_vowel[vowel_num] = \
			 max(max_substring_len_ending_with_vowel[vowel_num],max_substring_len_ending_with_vowel[prev_vowel_num]) + 1



	return max_substring_len_ending_with_vowel[4]


print (LIS('aeiaaioooaauuaeiou'))