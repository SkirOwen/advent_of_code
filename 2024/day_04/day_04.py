from __future__ import annotations

import itertools
from collections import Counter

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_grid(grid, matches, valid=(), starts=()):
	for y, row in enumerate(grid):
		for x, col in enumerate(row):
			if (x, y) in valid:
				if (x, y) in starts:
					print(f"{YELLOW}{col}{RESET}", end="")
				else:
					print(f"{GREEN}{col}{RESET}", end="")
			elif (x, y) in starts:
				print(f"{BLUE}.{RESET}", end="")
			elif (x, y) in matches:
				print(f"{RED}.{RESET}", end="")
			else:
				print(".", end="")
		print("")


def flatten_list(lst: list[list[any]]) -> list[any]:
	return list(itertools.chain(*lst))


def grid_get(grid, x, y, default = "."):
    if x < 0 or y < 0:
        return default
    try:
        return grid[y][x]
    except IndexError:
        return default


def grid_slice(grid, x, y, step):
	new_grid = [
		[grid_get(grid, xi, yi) for yi in range(y-step, y+step+1)]
		for xi in range(x-step, x+step+1)
	]
	return new_grid


def find_neighbours(grid, start: tuple, step:int, directions=("up",)):
	x, y = start

	possible_neighbour_idx = []

	for direction in directions:
		if direction == "up":
			word_idx = [(x, yi) for yi in range(y-1, y-step-1, -1)]

		if direction == "ul":
			word_idx = [(xi, yi) for xi, yi in zip(range(x+1, x+step+1), range(y-1, y-step-1, -1))]

		if direction == "le":
			word_idx = [(xi, y) for xi in range(x+1, x+step+1)]

		if direction == "dl":
			word_idx = [(xi, yi) for xi, yi in zip(range(x+1, x+step+1), range(y+1, y+step+1))]

		if direction == "do":
			word_idx = [(x, yi) for yi in range(y+1, y+step+1)]

		if direction == "dr":
			word_idx = [(xi, yi) for xi, yi in zip(range(x-1, x-step-1, -1), range(y+1, y+step+1))]

		if direction == "ri":
			word_idx = [(xi, y) for xi in range(x-1, x-step-1, -1)]

		if direction == "ur":
			word_idx = [(xi, yi) for xi, yi in zip(range(x-1, x-step-1, -1), range(y-1, y-step-1, -1))]

		word_idx.insert(0, start)
		# print("word_idx", word_idx)
		possible_neighbour_idx.append(word_idx)
	return possible_neighbour_idx


def check_neighbour(grid, pattern, possible_neighbour_idx) -> list:
	valid_neighbours = []

	for neighbour_idx in possible_neighbour_idx:
		safe = True
		for i, letter_idx in enumerate(neighbour_idx[1:]):
			letter = grid_get(grid, x=letter_idx[0], y=letter_idx[1])
			if letter != pattern[i]:
				safe = False
		if safe:
			valid_neighbours.append(neighbour_idx)
	return valid_neighbours


def find_sequence(grid, pattern="XMAS", directions=("up",), x_mode=False):
	matches_idx = []
	valid_idx = []
	starts = []
	occ = 0
	second_letters = []
	for y, row in enumerate(grid):
		for x, ele in enumerate(row):

			if ele == pattern[0]:
				step = len(pattern[1:])

				start = (x, y)
				starts.append(start)

				possible_neighbour_idx = find_neighbours(grid, start, step=step, directions=directions)
				valid_neighbours = check_neighbour(grid, pattern=pattern[1:], possible_neighbour_idx=possible_neighbour_idx)

				if x_mode:
					second_letter = [v[1] for v in valid_neighbours]
					second_letters.extend(second_letter)
				else:
					occ += len(valid_neighbours)
				valid_idx.extend(valid_neighbours)
				matches_idx.extend(possible_neighbour_idx)

	if x_mode:
		c = Counter(second_letters)
		occ = sum(v > 1 for v in c.values())
		
		new_valid = set([k for k, v in c.items() if v == 2])
		valid_idx = [v for v in valid_idx if v[1] in new_valid]

	print_grid(grid, flatten_list(matches_idx), flatten_list(valid_idx), starts)

	return occ


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]


	resutl1 = find_sequence(
		lines,
		directions=("up", "ul", "le", "dl", "do", "dr", "ri", "ur"),
		)
	print(f"Part I: {resutl1}")

	resutl2 = find_sequence(
		lines,
		pattern="MAS",
		directions=("ul", "dl", "dr", "ur"),
		x_mode=True,
	)

	
	print(f"Part II: {resutl2}")


if __name__ == "__main__":
	main()
