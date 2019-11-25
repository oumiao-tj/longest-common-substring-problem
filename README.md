Longest-common-substring-problem in Python
================================

Given a large number of binary files, to find the longest strand of bytes that is identical between two or more files is equivalent to the [longest 2-common substring problem](https://en.wikipedia.org/wiki/Longest_common_substring_problem).

I constructed a class GeneralizedSuffixTree which takes list[list[int]] as its input. Function self.find_longest_common_sublist returns length of the longest 2-common sublist and where it appears (including files and offset in each file).

How to use
----------

	lis0 = [1,3,6,3,5,7,3,9,5,7,3,5,7]
	lis1 = [2,4,6,8,2,1,5,2,7]
	lis2 = [4,6,8,2,3,8,3,3,7,8,4]
	tree = GeneralizedSuffixTree([lis0, lis1, lis2])
	print(tree.find_longest_common_sublist())
	
Output will be

	(4, [(1, -8), (2, -11)])
	
which means longest length of 2-common sublist = 4 and it appears in lis1 at index -8 (which is len(lis1) - 8 = 1) and lis2 at index -11 (which is len(lis2) - 11 = 0).

Usage note
----------

This library is mostly an academic exercise. 
If you need an efficient library
I would recommend a python-wrapped c implementation, 
such as [this one](http://www.daimi.au.dk/~mailund/suffix_tree.html).
