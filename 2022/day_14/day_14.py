import time

from itertools import pairwise
from typing import List, Optional


def line_parser(line: str) -> List:
	split_line = line.split()
	parsed_line = []
	for word in split_line:
		if word == "->":
			continue
		else:
			x, y = word.split(",")
			parsed_line.append([int(x), int(y)])
	return parsed_line


def gen_grid(lines: List, floor: bool) -> List:
	x_values = [coor[0] for path in lines for coor in path]
	y_values = [coor[1] for path in lines for coor in path]

	min_x = min(x_values)
	max_x = max(x_values)
	height = max(y_values)
	width = max_x - min_x

	if floor:
		height += 2
		width += 10
		min_x += 2

		
	grid = [["." for i in range(width + 1)] for j in range(height + 1)]
	grid[0][500 - min_x] = "+"

	for path in lines:
		for point1, point2 in pairwise(path):
			x1, y1 = point1[0] - min_x, point1[1]
			x2, y2 = point2[0] - min_x, point2[1]

			for x in range(min(x1, x2), max(x1, x2)+1):
				for y in range(min(y1, y2), max(y1, y2) +1):
					grid[y][x] = "#"
	if floor:
		for point in range(width + 1):
			grid[-1][point] = "#"

	return grid


def update_sand(grid: List, lines: List, sand_dropped: int) -> List:
	sand_x, sand_y = [500, 1]

	min_x = min([coor[0] for path in lines for coor in path])

	sand_x = sand_x - min_x
	is_moving = True
	sand_path = [[sand_x, sand_y]]

	while is_moving:
		# print(grid[sand_y][sand_x - 1: sand_x + 2])

		if sand_y > len(grid) - 1:
			is_moving = False
			return sand_path

		under = grid[sand_y + 1][sand_x - 1: sand_x + 2]
		# print(under)
		# print(under[:2])

		if len(under) < 3:
			is_moving = False
			return sand_path
		
		if under[1] == ".":
			# print(1)
			grid[sand_y][sand_x] = "."
			sand_x, sand_y = sand_x, sand_y + 1
			grid[sand_y][sand_x] = "o"

		elif under[:2] == [".", "o"] or under[:2] == [".", "#"]:
			# print(2)
			grid[sand_y][sand_x] = "."
			sand_x, sand_y = sand_x - 1, sand_y + 1
			grid[sand_y][sand_x] = "o"

		elif under[2] == ".":
			# print(3)
			grid[sand_y][sand_x] = "."
			sand_x, sand_y = sand_x + 1, sand_y + 1
			grid[sand_y][sand_x] = "o"
		else:
			# print(4)
			is_moving = False

		sand_path.append([sand_x, sand_y])
		time.sleep(0.001)
 
		for i in range(len(grid) + 4):
			print("\033[1A", end="\x1b[2K")
		draw(grid, lines, sand_dropped)

	# return sand_path


def simulate(grid: List, lines: List, sand_dropped: int) -> int:
	while True:
		sand_path = update_sand(grid, lines, sand_dropped)
		if sand_dropped == sand_dropped + 1 or sand_path is not None:
			break
		sand_dropped += 1

	draw(grid, lines, sand_dropped, sand_path)

	return sand_dropped


def draw(grid: List, lines: List, sand_dropped: int, sand_path: Optional = None) -> None:
	x_values = [coor[0] for path in lines for coor in path]
	
	min_x = min(x_values)
	max_x = max(x_values)

	height = len(grid)
	width = max_x - min_x

	if sand_path is not None:
		for point in sand_path:
			grid[point[1]][point[0]] = "~"

	padding = "".ljust(len(str(len(grid))))
	print(padding, *[x // 100 for x in range(min_x, max_x + 1)])
	print(padding, *[x // 10 % 10 for x in range(min_x, max_x + 1)])
	print(padding, *[x % 10 for x in range(min_x, max_x + 1)])

	for i, row in enumerate(grid):
		padding = str(i).ljust(len(str(len(grid))))
		print(padding, *row)

	print("\n")
	print(f"- Sand Dropped > {sand_dropped} <".center((len(str(len(grid)))) + len(grid[0])))
	print("\033[1A", end="\x1b[2K")
	print("\033[1A", end="\x1b[2K")


def main() -> None:
	filename = "test.txt"
	lines = []
	with open(filename, "r") as f:
		for line in f:
			lines.append(line_parser(line))

	# Part One
	sand_dropped = 0
	grid = gen_grid(lines, floor=False)
	draw(grid, lines, sand_dropped)
	sand_dropped = simulate(grid, lines, sand_dropped)
	print(	print(f"- Sand Dropped > {sand_dropped} <".center((len(str(len(grid)))) + len(grid[0]))))

	# Part Two
	sand_dropped = 0
	grid = gen_grid(lines, floor=True)
	draw(grid, lines, sand_dropped)
	sand_dropped = simulate(grid, lines, sand_dropped)
	print(	print(f"- Sand Dropped > {sand_dropped} <".center((len(str(len(grid)))) + len(grid[0]))))



if __name__ == "__main__":
	main()
