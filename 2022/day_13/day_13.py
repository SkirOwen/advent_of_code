import ast

from itertools import zip_longest
from functools import cmp_to_key
from typing import List 


def check_right_order(pair_0: List, pair_1) -> bool:
	# print(f"- Compare {pairs[0]} vs {pairs[1]}")
	
	for left, right in zip_longest(pair_0, pair_1, fillvalue=-1):
		# print(f"\t- Compare {left} vs {right}")

		if type(left) == int and type(right) == list:
			left = [left]
		elif type(left) == list and type(right) == int:
			right = [right]

		if type(left) == int and type(right) == int:
			if left < right:
				return -1
			elif left == right:
				continue
			elif left > right:
				return 1

		if type(left) == list and type(right) == list:
			# print("\t", end="")
			order = check_right_order(left, right)
			if order != 0:
				return order	

	if len(pair_0) > len(pair_1):
		return -1 
	elif len(pair_0) < len(pair_1):
		return 1
	return 0


def main() -> None:
	filename = "input.txt"

	lines = []
	with open(filename, "r") as f:
		pairs = []
		for line in f:
			# print(line) 
			if line == "\n":
				# print("")
				lines.append(pairs)
				pairs = []
			else:
				# print(line)
				pairs.append(ast.literal_eval(line))
		lines.append(pairs)

	# Part One
	s = []
	for i, pairs in enumerate(lines, start=1):
		# print(f"== Pair {i} ==")
		order = check_right_order(pairs[0], pairs[1])
		# print(order)
		# print("\n")
		if order == -1:
			s.append(i)

	# print(s)
	print(sum(s))
	# 5198

	# Part Two
	divider_packets = [[[2]], [[6]]]
	all_packets = sum(lines, [])

	all_packets.extend(divider_packets)
	
	sort_packets = sorted(all_packets, key=cmp_to_key(check_right_order))
	decoder_key = 1
	for i, v in enumerate(sort_packets, start=1):
		# print(v)
		if v in divider_packets:
			decoder_key *= i

	print(decoder_key)


if __name__ == "__main__":
	main()
