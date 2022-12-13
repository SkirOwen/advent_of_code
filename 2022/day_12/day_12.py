import time

from typing import List, Tuple


def get_neighbours(grid: List, current_point: List) -> List:
	current_height = grid[current_point[1]][current_point[0]]
	# print(current_point)
	neighbours = []
	for position in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
		node_position = (
			current_point[0] + position[0],
			current_point[1] + position[1]
			)

		x, y = node_position[0], node_position[1]
		if x >= len(grid[0]) or x < 0 or y >= len(grid) or y < 0:
			continue

		if ord(grid[y][x]) - ord(current_height) > 1:
			continue

		neighbours.append(node_position)

	return neighbours


def pathfinder(grid: List, start: List, end: List) -> List:
	open_list = []
	close_list = []

	open_list.append({
			"pos": start,
	 		"f": 0,
	 		"h": 0,
	 		"g": 0,
	 		"parent": None
	 	})
	previous_node = None

	while len(open_list) > 0:
		current_point = open_list[0]
		current_index = 0

		for index, point in enumerate(open_list):
			if point["f"] < current_point["f"]:
				current_point = point
				current_index = index

		# print(current_point["pos"])

		open_list.pop(current_index)
		close_list.append(current_point)
		close_list_position = [point["pos"] for point in close_list]

		path = []
		# Found path
		if current_point["pos"] == end:
			current = current_point
			while current is not None:
				# print(current)
				path.append(current["pos"])
				current = current["parent"]
			path.reverse()
			draw(
				[i[:] for i in grid],
				current_point,
				close_list,
				open_list,
				neighbours,
				start,
				end,
				path
			)
			return path

		# Look at neighbours
		neighbours = get_neighbours(grid=grid, current_point=current_point["pos"])
		for neighbour in neighbours:
			if neighbour in close_list_position:
				continue
			g = current_point["g"] + 1
			h = abs((current_point["pos"][0] - end[0])) + abs((current_point["pos"][1] - end[1]))
			f = g + h

			control_flag = 0
			for open_point in open_list:
				if neighbour == open_point["pos"] and g >= open_point["g"]:
					control_flag = 1

			if control_flag == 0:
				open_list.append({
				"pos": neighbour,
				"f": f,
				"h": h,
				"g": g,
				"parent": current_point
				})

		draw(
			[i[:] for i in grid],
			current_point,
			close_list,
			open_list,
			neighbours,
			start,
			end,
			path
		)


def draw(canvas: List, current_point: List, close_list: List, open_list: List, neighbours: List, start: Tuple, end: Tuple, path: List) -> None:
	light_green = "\033[0;92m"
	orange = "\033[0;33m"
	pure_red = "\033[0;31m"
	dark_cyan = "\033[0;36m"
	dark_blue = "\033[0;34m"
	reset_colour = "\033[0m"

	
	for point in close_list:
		x, y = point["pos"][0], point["pos"][1]
		if x == current_point["pos"][0] and y == current_point["pos"][1]:
			colour = orange
		else:
			colour = light_green
		canvas[y][x] = colour + canvas[y][x] + reset_colour

	for point in open_list:
		x, y = point["pos"][0], point["pos"][1]
		if point["pos"] in neighbours:
			colour = dark_blue
		else:
			colour = pure_red
		canvas[y][x] = colour + canvas[y][x] + reset_colour

	canvas[start[1]][start[0]] = dark_cyan + "S" + reset_colour
	canvas[start[1]][start[0]] = dark_cyan + "E" + reset_colour

	for pix in canvas:
		print(*pix)
	
	for i in range(len(canvas)):
		print("\033[1A", end="\x1b[2K")

	time.sleep(0.001)
	if len(path) > 0:
		for point in path:
			x, y = point[0], point[1]
			canvas[y][x] = dark_cyan + "*" + reset_colour
		for pix in canvas:
			print(*pix)


def get_a_coord(grid: List) -> List:
	a_coord = []
	for y, grid_y in enumerate(grid):
		for x, grid_x in enumerate(grid_y):
			if grid_x == "a":
				a_coord.append([x, y])
	return a_coord 


def main() -> None:
	filename = "input.txt"

	grid = []
	with open(filename, "r") as f:
		for y, line in enumerate(f):
			grid_y = list(line.strip())
			# print(grid_y)
			if "S" in grid_y:
				start = (grid_y.index("S"), y)
				grid_y[start[0]] = "a"
			if "E" in grid_y:
				end = (grid_y.index("E"), y)
				grid_y[end[0]] = "z"

			grid.append(grid_y)


	# Part One
	path = pathfinder(grid, start, end)
	print(path)
	print(len(path)-1)

	# Part Two
	# a_list = get_a_coord(grid)
	a_list = [(0, i) for i in range(len(grid))]
	potential_path = []
	for a_coord in a_list[::-1]:
		path = pathfinder(grid, a_coord, end)
		if path is not None:
			potential_path.append(len(path)-1)
	print(potential_path)
	print(min(potential_path))

if __name__ == "__main__":
	main()
