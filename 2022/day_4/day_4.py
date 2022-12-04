import re

from typing import Tuple

def check_subset(range1: Tuple, range2: Tuple) -> bool:
	range2_subset_of_1 = range1[0] <= range2[0] and range1[1] >= range2[1]
	range1_subset_of_2 = range2[0] <= range1[0] and range2[1] >= range1[1]
	return range2_subset_of_1 or range1_subset_of_2


def check_overlap(range1: Tuple, range2: Tuple) -> bool:
	return range1[0] <= range2[1] and range1[1] >= range2[0]


def main() -> None:
	filename = "input.txt"

	nbr_fully_contained_range = 0
	nbr_overlap_range = 0

	with open(filename, "r") as f:
		for line in f:
			splitted_line = list(map(int, re.split("-|,|\n", line)[:-1]))	# [:-1] to remove the last element, which become "" with the split
			fst_pair, scd_pair = splitted_line[:2], splitted_line[2:]

			# Part One
			if check_subset(fst_pair, scd_pair):
				nbr_fully_contained_range += 1

			# Part Two
			if check_overlap(fst_pair, scd_pair):
				nbr_overlap_range += 1

	print(f"{nbr_fully_contained_range = }")
	print(f"{nbr_overlap_range = }")


if __name__ == '__main__':
	main()
