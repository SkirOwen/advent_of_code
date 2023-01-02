from math import lcm
from itertools import cycle
from typing import Iterator
from copy import deepcopy


def lines_parser(lines: list) -> list:
	blizzards = []

	for b, line in enumerate(lines):
		for a, c in enumerate(line):
			if c == ">":
				blizzards.append([complex(a, b), 0])
			elif c == "v":
				blizzards.append([complex(a, b), 1])
			elif c == "<":
				blizzards.append([complex(a, b), 2])
			elif c == "^":
				blizzards.append([complex(a, b), 3])

	return blizzards


def get_grid(lines: list) -> list:
	height = len(lines)
	width = len(lines[0])

	grid = [["." for x in range(width)] for y in range(height)]

	for i in range(height):
		grid[i][0] = "#"
		grid[i][width - 1] = "#"

	for i in range(2, width):
		grid[0][i] = "#"
		grid[height - 1][i - 2] = "#"

	return grid


def get_time_grid(grid, blizzards: list) -> list:
	time_grid = [blizzards.copy()]
	current_blizzards = blizzards

	width = len(grid[0])
	height = len(grid)

	reset_time = lcm(height - 2 , width - 2)

	for i in range(1, reset_time):
		new_blizards = []

		for blizzard in current_blizzards:
			if blizzard[1] == 0:
				mov = 1
			elif blizzard[1] == 1:
				mov = 1j
			elif blizzard[1] == 2:
				mov = -1
			else:
				mov = -1j

			new_pos = blizzard[0] + mov
			if new_pos.real == 0:
				new_pos = complex(width - 2, new_pos.imag)

			elif new_pos.real == width - 1:
				new_pos = complex(1, new_pos.imag)

			elif new_pos.imag == 0:
				new_pos = complex(new_pos.real, height - 2)

			elif new_pos.imag == height - 1:
				new_pos = complex(new_pos.real, 1)

			new_blizards.append([new_pos, blizzard[1]])

		time_grid.append(new_blizards.copy())
		current_blizzards = new_blizards

	return time_grid


def draw(
		grid: list,
		blizzards: list,
		pos: None | complex = None,
		neighbours: None | list = None,
		close_list: None | list = None,
		stack: None | list = None,
		parent: None | list = None
	) -> None:

	red = "\033[0;31m"
	green = "\033[0;92m"
	blue = "\033[0;34m"
	orange = "\033[0;33m"
	cyan = "\033[0;96m"
	reset_colour = "\033[0m"

	canvas = deepcopy(grid)
	blizzards_pos = [b[0] for b in blizzards]

	for blizzard in blizzards:
		a, b = int(blizzard[0].real), int(blizzard[0].imag)
		
		rot = blizzard[1]
		if rot == 0:
			symbol = ">"
		elif rot == 1:
			symbol = "v"
		elif rot == 2:
			symbol = "<"
		else:
			symbol = "^"

		nbr = str(blizzards_pos.count(blizzard[0]))

		canvas[b][a] = symbol if canvas[b][a] == "." else nbr

	if close_list is not None:
		for c in close_list:
			a, b = int(c[1].real), int(c[1].imag)
			canvas[b][a] = green + canvas[b][a] + reset_colour

	if stack is not None:
		for s in stack:
			a, b = int(s[1].real), int(s[1].imag)
			canvas[b][a] = orange + canvas[b][a] + reset_colour

	if parent is not None:
		for p in parent:
			a, b = int(p.real), int(p.imag)
			canvas[b][a] = cyan + canvas[b][a] + reset_colour

	if neighbours is not None:
		for n in neighbours:
			a, b = int(n.real), int(n.imag)
			canvas[b][a] = blue + "N" + reset_colour

	if pos is not None:
		a, b = int(pos.real), int(pos.imag)
		canvas[b][a] = red + "E" + reset_colour

	for row in canvas:
		print(*row)

	print("\033[1A" * (len(canvas) + 2), end="\x1b[2K")


def get_neighbour(t, pos, time_grid, width, height, start, end) -> Iterator:
	idx = t % len(time_grid)

	blizzards = time_grid[idx]
	blizzards_pos = [b[0] for b in blizzards]

	pot_moves = [1, -1, 1j, -1j, 0]

	for pot_mov in pot_moves:
		n = pos + pot_mov

		if n != end and n != start:
			if n in blizzards_pos or (n.real <= 0) or (n.imag <= 0) or (n.real >= (width - 1)) or (n.imag >= (height - 1)):
				continue
		
		yield n


def pathfinder(start_t: int, time_grid: list, start: complex, end: complex, grid: list, forward: bool = True) -> int:
	width = len(grid[0])
	height = len(grid)

	if forward:
		start_point = start
		end_point = end
	else:
		start_point = end
		end_point = start

	# stack = [(start_t, start_point, 0, 0, 0, [])]
	stack = [(start_t, start_point, [])]
	close_list = []
	close_draw = []

	while stack:
		current_point = stack[0]
		current_index = 0

		# for index, point in enumerate(stack):
		# 	if point[4] < current_point[4] and point[0] < current_point[0]:
		# 		current_point = point
		# 		current_index = index

		# t, pos, g, h, f, parent = stack.pop()
		t, pos, parent = stack.pop(0)
		close_list.append((t % len(grid), pos))
		# close_list.append((t % len(grid), pos))

		if pos == end_point:
			return t

		neighbours = get_neighbour(t+1, pos, time_grid, width, height, start_point, end_point)
		new_points = []
		for n in neighbours: 
			# TODO: heuristic 
			# new_g = g + 1
			# new_h = abs(pos.real - end_point.real) + abs(pos.imag - end_point.imag)
			# new_f = g + h
			
			parent.append(pos)
			# new_step = (t+1, n, new_g, new_h, new_f, parent)
			new_step = (t+1, n, parent)

			if ((t+1 % len(time_grid), n)) in close_list:
				continue

			control_flag = 0
			for point in stack:
				if  (new_step[0] % len(time_grid)) == (point[0] % len(time_grid)) and new_step[1] == point[1]: # and g >= point[2]:
					control_flag = 1

			if control_flag == 0:
				new_points.append(n)

				stack.append(new_step)

		if pos not in close_draw:
			print("")
			print(f"time {t}")
			t1 = t % len(time_grid)
			draw(grid, time_grid[t1], pos, new_points, close_list, stack)

		close_draw.append(pos)


def main() -> None:
	filename = "input.txt"

	lines = []

	with open(filename, "r") as f:
		for line in f:
			lines.append(line.strip())

	height = len(lines)
	width = len(lines[0])

	start = complex(1, 0)
	end = complex(width - 2, height - 1)
	blizzards = lines_parser(lines)
	grid = get_grid(lines)

	time_grid = get_time_grid(grid, blizzards)

	t_final = pathfinder(0, time_grid, start, end, grid, forward=True)
	print("part one", t_final)

	t_back = pathfinder(t_final, time_grid, start, end, grid, forward=False)
	print(t_back - t_final)

	t_tot = pathfinder(t_back, time_grid, start, end, grid, forward=True)
	print(t_tot - t_back)

	print("total time:", t_tot)


if __name__ == "__main__":
	main()
