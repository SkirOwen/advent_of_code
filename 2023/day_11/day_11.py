from __future__ import annotations

from itertools import accumulate, combinations


def get_row_col_idx(lines: list, expanse: int = 2) -> tuple[list[int], list[int]]:
	row = [expanse for i in range(len(lines))]
	col = [expanse for i in range(len(lines[0]))]

	for i, (line, r) in enumerate(zip(lines, row)):
		if "#" in line:
			row[i] = 1

	for j, (char, c) in enumerate(zip(range(len(lines[0])), col)):
		column = []
		for i, (line, r) in enumerate(zip(range(len(lines)), row)):
			column.append(lines[i][j])
		print(column)
		if "#" in column:
			col[j] = 1

	row = list(accumulate(row))
	col = list(accumulate(col))

	return row, col


def get_galaxy_pos(row: list[int], col: list[int], lines: list[str]) -> list[tuple[int, int]]:
	pos = []
	for i, (line, r) in enumerate(zip(lines, row)):
		for j, (char, c) in enumerate(zip(line, col)):
			if char == "#":
				pos.append((r, c))
	return pos


def draw(lines, row, col):
	print("  ", end="")
	for c in col:
		print(f'{c:2d}', end=" ")
	print()
	for line, r in zip(lines, row):
		print(f'{r:2d}', end=" ")
		for char in line:
			print(f'{char:2}', end=" ")
		print()


def galaxy_dist(galaxy_pos):
	distances = {k: [] for k in galaxy_pos}
	for a, b in combinations(galaxy_pos, 2):
		dist = (abs(a[0] - b[0])) + (abs(a[1] - b[1]))
		distances[a].append(dist)
	return distances


def get_sum_galaxy_dist(lines, expanse):
	row, col = get_row_col_idx(lines, expanse)
	draw(lines, row, col)
	galaxy_pos = get_galaxy_pos(row, col, lines)
	distances = galaxy_dist(galaxy_pos)
	min_dist = [v for val in distances.values() for v in val]

	return min_dist


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	min_dist = get_sum_galaxy_dist(lines, expanse=2)
	print(f"Part I: {sum(min_dist)}")

	min_dist = get_sum_galaxy_dist(lines, expanse=1_000_000)
	print(f"Part II: {sum(min_dist)}")


if __name__ == "__main__":
	main()
