from __future__ import annotations

import time

from collections import deque



def gen_grid(lines: list[tuple[int, int]], nbr_byte: int, size: tuple[int, int]) -> list[list[str]]:

	grid = [
		["." for x in range(size[0] + 1)] 
		for y in range(size[1] + 1)
	]

	for i, line in enumerate(lines):
		if i >= nbr_byte:
			break
		x, y = line
		grid[y][x] = "#"


	return grid


def get_neighbours(grid, pos) -> list[tuple[int, int]]:

	neighbours = []

	for next_step in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
		forward_move = (
			pos[0] + next_step[0],
			pos[1] + next_step[1],
		)
		x, y = forward_move

	# Check if the forward move is valid (within bounds and not blocked)
		if 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] != "#":
			neighbours.append(forward_move)

	return neighbours


def pathfind(lines: list, start: tuple[tuple[int, int], str], end: tuple[int, int], draw: bool = True) -> list:

	queue = deque([{"path": [start]}])  
	visited = []

	complete_path = []
	k = 0

	while queue:
		state = queue.popleft()
		current_pos = state["path"][-1]

		if current_pos in visited:
			continue

		visited.append(current_pos)

		# Path found
		x, y = current_pos
		if (x, y) == end:
			complete_path.append(state["path"])
			continue

		neighbours = get_neighbours(lines, current_pos)
		for neighbour in neighbours:

			queue.append({
				"path": state["path"] + [neighbour],
				})

		if draw and k % 200 == 0:
			draw(
				canvas=[i[:] for i in lines],
				current_point=state,
				close_list=visited,
				open_list=queue,
				neighbours=neighbours,
				start=start,
				end=end,
				# path
			)

		k += 1

	return complete_path


def draw(canvas: list, current_point: list, close_list: list, open_list: list, neighbours: list, start: tuple, end: tuple) -> None:
	light_green = "\033[0;92m"
	orange = "\033[0;33m"
	pure_red = "\033[0;31m"
	dark_cyan = "\033[0;36m"
	light_cyan = "\033[0;96m"
	dark_blue = "\033[0;34m"
	cyan_back = "\033[0;46m"
	reset_colour = "\033[0m"

	# Prepare to build the current path
	current_path = current_point["path"]

	for point in open_list:
		x, y = point["path"][-1]  # Extract the position from the last step in the path
		if point["path"][-1] in neighbours:
			colour = dark_blue
		elif point["path"][-1] in current_path:
			colour = light_cyan
		else:
			colour = pure_red
		canvas[y][x] = colour + "█" + reset_colour

	# Colour close list
	for point in close_list:
		x, y = point  # Extract the position
		if (x, y) == current_point["path"][-1][0]:  # Match the current point
			colour = orange
		elif point in current_path:
			colour = light_cyan
		else:
			colour = light_green
		canvas[y][x] = colour + "█" + reset_colour

	# Colour start and end
	canvas[start[1]][start[0]] = dark_cyan + "S" + reset_colour
	canvas[end[1]][end[0]] = dark_cyan + "E" + reset_colour

	# Print the canvas
	for row in canvas:
		print(" ".join(row))

	# Wait and clear output
	time.sleep(0.01)
	print("\033[1A" * len(canvas), end="\x1b[2K")


def draw_completed_path(canvas: list, path: list, start: tuple, end: tuple) -> None:
	"""
	Draws the completed path on the canvas.

	Args:
		canvas (list[list[str]]): The grid as a list of lists.
		path (list[tuple[tuple[int, int], str]]): The completed path as a list of (position, facing).
		start (tuple[tuple[int, int], str]): The starting position and facing direction.
		end (tuple[int, int]): The end position as a tuple (x, y).
	"""
	# Colour codes
	light_green = "\033[0;92m"
	cyan_back = "\033[0;46m"
	dark_cyan = "\033[0;36m"
	reset_colour = "\033[0m"

	# Make a copy of the canvas to modify
	visual_canvas = [row[:] for row in canvas]

	# Draw the path
	for step in path:
		pos = step  # Extract position (x, y)
		x, y = pos
		if (x, y) == start:
			continue  # Skip the start position
		if (x, y) == end:
			continue  # Skip the end position
		visual_canvas[y][x] = cyan_back + "█" + reset_colour

	# Highlight start and end positions
	visual_canvas[start[1]][start[0]] = dark_cyan + "S" + reset_colour
	visual_canvas[end[1]][end[0]] = light_green + "E" + reset_colour

	# Print the canvas
	for row in visual_canvas:
		print(" ".join(row))


def find_when_blocked(lines: list, start: tuple, end: tuple) -> tuple[int, int]:
	nbr_byte = 1024

	while True:
		grid = gen_grid(lines, nbr_byte, end)
		paths = pathfind(grid, start=(0, 0), end=end, draw=False)

		if len(paths) == 0:
			break
		draw_completed_path(grid, paths[0], start=start, end=end)

		nbr_byte += 1

	return lines[nbr_byte - 1]



def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [tuple(map(int, line.strip().split(","))) for line in f]

	end = (70, 70)
	start = (0, 0)

	grid = gen_grid(lines, 1024, end)
	paths = pathfind(grid, start=start, end=end)

	print()
	draw_completed_path(grid, paths[0], start=start, end=end)
	print(f"Part I: {min(map(len, paths)) - 1}")

	blocked_byte = find_when_blocked(lines, start=start, end=end)
	print("Part II:", blocked_byte)

if __name__ == "__main__":
	main()
