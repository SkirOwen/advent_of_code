from typing import List

class Point():
	def __init__(self, position, parent) -> None:
		self.parent = parent
		self.position = position

		self.g = 0
		self.f = 0
	
	def __eq__(self, other) -> bool:
		return self.position == other.position



def get_neighbours(grid: List, current_point: Point) -> List:
	current_height = grid[current_point.position[1]][current_point.position[0]]
	# print(current_point)
	neighbours = []
	for position in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
		node_position = (
			current_point.position[0] + position[0],
			current_point.position[1] + position[1]
			)

		x, y = node_position[0], node_position[1]
		if x >= len(grid[0]) or x < 0 or y >= len(grid) or y < 0:
			continue

		if abs(ord(current_height) - ord(grid[y][x])) > 1:
			continue

		neighbours.append(Point(position=node_position, parent=current_point))

	return neighbours


def pathfinder(grid: List, start: List, end: List) -> List:
	open_list = []
	close_list = []

	open_list.append(Point(position=start, parent=None))

	while len(open_list) > 0:
		current_point = open_list[0]
		current_index = 0

		for index, point in enumerate(open_list):
			if point.f < current_point.f:
				current_point = point
				current_index = index

		# print(current_point["pos"])

		open_list.pop(current_index)
		close_list.append(current_point)
		# close_list_position = [point.position for point in close_list]

		# print(open_list)

		# Found path
		if current_point.position == end:
			print("a")
			path = []
			current = current_point
			while current is not None:
				# print(current)
				path.append(current.position)
				current = current.parent
			path.append(start)
			path.reverse()
			print(f"Path found: {path}")
			return path

		# Look at neighbours
		neighbours = get_neighbours(grid=grid, current_point=current_point)
		for neighbour in neighbours:
			if neighbour in close_list:
				continue
			neighbour.g = current_point.g + 1
			neighbour.h = 0
			neighbour.f = neighbour.g + neighbour.h
			for open_point in open_list:
				if neighbour == open_point and neighbour.g > open_point.g:
					continue
			open_list.append(neighbour)



def main() -> None:
	filename = "input.txt"

	grid = []
	with open(filename, "r") as f:
		for y, line in enumerate(f):
			grid_y = list(line.strip())
			print(grid_y)
			if "S" in grid_y:
				start = (grid_y.index("S"), y)
				grid_y[start[0]] = "a"
			if "E" in grid_y:
				end = (grid_y.index("E"), y)
				grid_y[end[0]] = "z"

			grid.append(grid_y)

	print(*grid)
	print(start, end)
	path = pathfinder(grid, start, end)
	print(path)
	


if __name__ == "__main__":
	main()
