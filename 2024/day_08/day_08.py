from __future__ import annotations

import itertools as it
from collections import defaultdict



def find_antinode(locs: list, size: tuple[int, int], gridpoint: bool = False) -> list:
	antinode = []
	for loc1, loc2 in it.combinations(locs, 2):
		x1, y1 = loc1
		x2, y2 = loc2
		
		dy = y2 - y1
		dx = x2 - x1

		m = dy/dx
		c = y1 - (m * x1)  

		if not gridpoint:
			anti1 = (x1 - dx, round(m * (x1 - dx) + c))
			anti2 = (x2 + dx, round(m * (x2 + dx) + c))

			if (0 <= anti1[0] < size[0]) and (0 <= anti1[1] < size[1]):
				antinode.append(anti1)
			if (0 <= anti2[0] < size[0]) and (0 <= anti2[1] < size[1]):
				antinode.append(anti2)

		else:
			for x in range(size[0]):
				y_grid = m * x + c

				if abs(y_grid - round(y_grid)) < 1e-5:
					if 0 <= round(y_grid) < size[1]:
						antinode.append((x, round(y_grid)))
			
	return antinode


def find_all_antinode(antennas: dict, size: tuple[int, int], gridpoint: bool = False) -> list:
	antinodes = []

	for antenna_id, antenna_locs in antennas.items():
		
		if len(antenna_locs) > 1:
			antinode = find_antinode(antenna_locs, size, gridpoint)
			antinodes.extend(antinode)

	return antinodes


def parse(lines: list) -> dict:
	antennas = defaultdict(list)

	for y, line in enumerate(lines):
		for x, char in enumerate(line):
			if char != ".":
				antennas[char].append((x, y))

	return antennas


def print_node(lines: list, antinodes: list) -> None:
	for y, line in enumerate(lines):
		for x, char in enumerate(line):
			if char != ".":
				print(f"\033[31m{char}\033[0m", end="")
			elif (x, y) in antinodes:
				print("\033[33m#\033[0m", end="")
			else:
				print(".", end="")
		print("")



def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	antennas = parse(lines)
	size = (len(lines[0]), len(lines))
	
	antinodes = find_all_antinode(antennas, size, gridpoint=False)

	print_node(lines, antinodes)
	print(f"Part I: {len(set(antinodes))}")

	antinodes_gridpoint = find_all_antinode(antennas, size, gridpoint=True)

	print_node(lines, antinodes_gridpoint)
	print(f"Part II: {len(set(antinodes_gridpoint))}")


if __name__ == "__main__":
	main()
