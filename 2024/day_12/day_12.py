from __future__ import annotations

from collections import Counter


def find_plots(lines: list[list[str]]) -> list[set[tuple[int, int]]]:
	plots = []
	seen = set()

	for y, line in enumerate(lines):
		for x, char in enumerate(line):
			if (x, y) not in seen:
				plot = [(x, y)]
				pos = 0
				while pos < len(plot):

					i, j = plot[pos]
					for x1, y1 in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
						if 0 <= x1 < len(lines[0]) and 0 <= y1 < len(lines):
							if (x1, y1) not in seen and (x1, y1) not in plot and lines[j][i] == lines[y1][x1]:
								plot.append((x1, y1))
								seen.add((x1, y1))
					pos += 1
				plots.append(set(plot))
	return plots


def find_edges(plot: set[tuple[int, int]]) -> dict:
	edges = {}
	for pos in plot:
		x, y = pos
		up    = (x      , y + 0.5)
		left  = (x - 0.5, y)
		right = (x + 0.5, y)
		down  = (x      , y - 0.5)
		edges[str(pos)] = [up, left, right, down]
	return edges


def calculate_perimeter(plot: set[tuple[int, int]]) -> int:
	edges = find_edges(plot)
	all_edges = sum([v for k, v in edges.items()], [])
	perimeter_edges = [edge for edge in all_edges if all_edges.count(edge) == 1]
	return len(perimeter_edges)


def price_plot(plot: set[tuple[int, int]]) -> int:
	area = len(plot)
	perimeter = calculate_perimeter(plot)
	return area * perimeter


def price_total(plots: list[set[tuple[int, int]]]) -> int:
	tot = 0
	for plot in plots:
		tot += price_plot(plot)
	return tot


def calculate_sides(plot: set[tuple[int, int]]) -> int:
	edges = 0
	for pos in plot:
		x, y = pos
		u = (x    , y - 1)
		l = (x - 1, y    )
		d = (x    , y + 1)
		r = (x + 1, y    )

		ul = (x - 1, y - 1)
		ur = (x + 1, y - 1)
		dl = (x - 1, y + 1)
		dr = (x + 1, y + 1)
		
		if u not in plot and l not in plot:
			edges += 1
		if l not in plot and d not in plot:
			edges += 1
		if d not in plot and r not in plot:
			edges += 1
		if r not in plot and u not in plot:
			edges += 1

		if u in plot and l in plot and ul not in plot:
			edges += 1
		if l in plot and d in plot and dl not in plot:
			edges += 1
		if d in plot and r in plot and dr not in plot:
			edges += 1
		if r in plot and u in plot and ur not in plot:
			edges += 1


	return edges

	return len(side_number)


def price_bulk_plot(plot: set[tuple[int, int]]) -> int:
	area = len(plot)
	perimeter = calculate_sides(plot)
	print(area, perimeter, area * perimeter)
	return area * perimeter


def price_bulk_total(plots: list[set[tuple[int, int]]]) -> int:
	tot = 0
	for plot in plots:
		tot += price_bulk_plot(plot)
	return tot


def draw(lines, plots) -> None:
	RED = "\033[0;31m"
	GREEN = "\033[0;32m"
	BROWN = "\033[0;33m"
	BLUE = "\033[0;34m"
	END = "\033[0m"

	for y, line in enumerate(lines):
		for x, char in enumerate(line):
			for colour, plot in zip([RED, GREEN, BLUE], plots):
				if (x, y) in plot:
					print(f"{colour}{char}{END}", end="")
		print()



def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [list(line.strip()) for line in f]

	# lines = [
	# ["A", "A", "A"],
	# ["A", "B", "B"],
	# ]

	plots = find_plots(lines)
	print(plots)
	# print(len(plots))

	draw(lines, plots)

	result1 = price_total(plots)
	print(f"Part I: {result1}")

	result2 = price_bulk_total(plots)
	print(f"Part 2: {result2}")


if __name__ == "__main__":
	main()
