from __future__ import annotations

from tqdm import tqdm

from concurrent.futures import ProcessPoolExecutor
from functools import partial


def grid(lines, visited, loop_obstacle=()):
	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			if (x, y) in loop_obstacle:
				print("O", end="")
			elif (x, y) in visited:
				print("X", end="")
			else:
				print(c, end="")
		print()


def next_step(pos, obstacles, lines):
	x_max = len(lines[0])
	y_max = len(lines)
	
	loc, direction = pos
	x, y = loc

	if direction == "up":
		new_loc = (x, y-1)
	elif direction == "ri":
		new_loc = (x+1, y)
	elif direction == "do":
		new_loc = (x, y+1)
	elif direction == "le":
		new_loc = (x-1, y)

	if new_loc[0] < 0 or new_loc[1] < 0 or new_loc[0] >= x_max or new_loc[1] >= y_max:
		return False

	if new_loc in obstacles:
		new_loc = loc

		if direction == "up":
			new_direction = "ri"
		elif direction == "ri":
			new_direction = "do"
		elif direction == "do":
			new_direction = "le"
		elif direction == "le":
			new_direction = "up"
	else:
		new_direction = direction

	new_pos = (new_loc, new_direction)


	return new_pos


def move_guard(start, obstacles, lines):
	pos = start
	visited = []
	while pos:
		visited.append(pos)
		pos = next_step(pos, obstacles, lines)
	return visited


def find_start_obstacles(lines: list) -> tuple[tuple[tuple[int, int], str], set[tuple[int, int]]]:
	obstacles = []
	for y, line in enumerate(lines):
		for x, char in enumerate(line):
			if char == "#":
				obstacles.append((x, y))
			elif char in [">", "<", "v", "^"]:
				if char == "^":
					start = ((x, y), "up")
				if char == "<":
					start = ((x, y), "le")
				if char == ">":
					start = ((x, y), "ri")
				if char == "v":
					start = ((x, y), "do")
	return start, set(obstacles)



def test_loop_location(v, start, obstacles, lines):
	new_obstacles = obstacles.copy()
	new_obstacles.add(v[0])

	pos = start
	visited = []
	while pos:
		visited.append(pos)
		pos = next_step(pos, new_obstacles, lines)
		if pos in visited:
			return v[0]
	return None



def find_loop_location(visited, start, obstacles, lines) -> set:


	# loop_obstacle = []

	# for v in tqdm(visited[1:]):
		# new_obstacles = obstacles.copy()
		# new_obstacles.add(v[0])

		# # print(new_obstacles)

		# pos = start
		# visited = []
		# while pos:
		# 	visited.append(pos)
		# 	pos = next_step(pos, new_obstacles, lines)
		# 	if pos in visited:
		# 		loop_obstacle.append(v[0])
		# 		

	partial_process_vertex = partial(test_loop_location, start=start, obstacles=obstacles, lines=lines)

	with ProcessPoolExecutor() as executor:
		loop_obstacle = list(
			tqdm(
				executor.map(
					partial_process_vertex,
					visited[1:],
				),
			total=len(visited[1:])
			)
		)

	return set(filter(None, loop_obstacle))



def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [list(line.strip()) for line in f]

	# grid(lines)

	start, obstacles = find_start_obstacles(lines)
	# print(start)
	# print(obstacles)
	visited = move_guard(start, obstacles, lines)
	visited_loc = set([v[0] for v in visited])
	# print(visited)

	grid(lines, visited_loc)

	loop_obstacle = find_loop_location(visited, start, obstacles, lines)

	print(f"Part I: {len(visited_loc)}")

	print(f"Part II: {len(loop_obstacle)}")

	grid(lines, visited_loc, loop_obstacle)
	# print(loop_obstacle)


if __name__ == "__main__":
	main()
