from __future__ import annotations

import re

def check_invalid_id(nbr: int, at_least_twice: bool = False) -> bool:
	match = r"^(\d+)\1$"

	if at_least_twice:
		match = r"^(\d+)\1+$"

	return bool(re.search(match, str(nbr)))



def find_repeats_in_nbrs(nbrs, at_least_twice: bool = False) -> list[int]:
	repeats = []
	for nbr in nbrs:
		if check_invalid_id(nbr, at_least_twice):
			repeats.append(nbr)

	return repeats



def find_repeats_in_ranges(id_ranges: list(int, int), at_least_twice: bool = False) -> list[int]:

	repeats = []

	for id_range in id_ranges:
		nbrs = range(id_range[0], id_range[1]+1)
		new_repeats = find_repeats_in_nbrs(nbrs, at_least_twice)

		repeats.extend(new_repeats)

	return repeats



def get_id_ranges(lines):

	id_ranges = []

	for line in lines:
		id_ranges.append(tuple(map(int, line.split("-"))))

	return id_ranges


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readline().strip().split(",")


	id_ranges = get_id_ranges(lines)
	print(id_ranges)

	repeats = find_repeats_in_ranges(id_ranges)

	print(sum(repeats))

	repeats = find_repeats_in_ranges(id_ranges, at_least_twice=True)

	print(sum(repeats))



if __name__ == "__main__":
	main()
