files = [] # a list which stores list[int] read from the binary files
for i in range(10):
	# reads 'sample.1' to 'sample.10' and stores them as list[int] in files
	files.append(list(open('sample.' + str(i+1), 'br').read()))

for i in range(10):
    print(f'Length of sample.{i+1} is {len(files[i])}')
# Desired output:
"""
Length of sample.1 is 17408
Length of sample.2 is 30720
Length of sample.3 is 45056
Length of sample.4 is 30720
Length of sample.5 is 23552
Length of sample.6 is 27648
Length of sample.7 is 21504
Length of sample.8 is 20480
Length of sample.9 is 13312
Length of sample.10 is 14336
"""

tree = GeneralizedSuffixTree(files) # Builds GeneralizedSuffixTree for files

res = tree.find_longest_common_sublist()
print(res)
# Desired output:
"""
(27648, [(1, -27648), (2, -27648)])
"""

# Let's make the meaning of output more clear
print(f'Length of the longest strand of bytes that exists in at least two files is: {res[0]}')
for i in range(len(res[1])):
    print(f'It appears at offset {len(files[res[1][i][0]]) + res[1][i][1]} in binary file sample.{res[1][i][0]+1}')
# Desired output:
"""
Length of the longest strand of bytes that exists in at least two files is: 27648
It appears at offset 3072 in binary file sample.2
It appears at offset 17408 in binary file sample.3
"""
