from __future__ import annotations

import time

from collections import deque, Counter


def find_start(lines: list[list[str]]) -> tuple[tuple[int, int], str]:
	for y, line in enumerate(lines):
		for x, char in enumerate(line):
			if char == "S":
				return ((x, y), "E")



def find_end(lines: list[list[str]]) -> tuple[int, int]:
	for y, line in enumerate(lines):
		for x, char in enumerate(line):
			if char == "E":
				return (x, y)


def get_neighbours(grid, pos, facing):
	# Directions with their respective (dx, dy) offsets
	DIRECTIONS = ["N", "E", "S", "W"]
	MOVES = {
		"N": (0, -1),
		"E": (1, 0),
		"S": (0, 1),
		"W": (-1, 0),
	}

	# Get the index of the current facing direction
	facing_idx = DIRECTIONS.index(facing)

	# Neighbouring moves: forward, turn left, and turn right
	forward_move = ((pos[0] + MOVES[facing][0], pos[1] + MOVES[facing][1]), facing)
	left_turn = (pos, DIRECTIONS[(facing_idx - 1) % 4])  # Rotate left
	right_turn = (pos, DIRECTIONS[(facing_idx + 1) % 4])  # Rotate right

	neighbours = []

	# Check if the forward move is valid (within bounds and not blocked)
	if 0 <= forward_move[0][1] < len(grid) and 0 <= forward_move[0][0] < len(grid[0]) and grid[forward_move[0][1]][forward_move[0][0]] != "#":
		neighbours.append(forward_move)

	# Add the rotations (turning does not move the position, so they are always valid)
	neighbours.append(left_turn)
	neighbours.append(right_turn)

	return neighbours


def pathfind(lines: list, start: tuple[tuple[int, int], str], end: tuple[int, int]):

	queue = deque([{"path": [start], "score": 0}])  
	visited = {}

	complete_path = []
	k = 0

	while queue:
		state = queue.popleft()
		current_pos = state["path"][-1]
		current_score = state["score"]

		if current_pos in visited and visited[current_pos] < current_score:
			continue

		visited[current_pos] = current_score

		# Path found
		x, y = current_pos[0]
		if (x, y) == end:
			complete_path.append(state["path"])
			continue

		neighbours = get_neighbours(lines, current_pos[0], current_pos[1])
		for neighbour in neighbours:
			new_score = current_score

			if neighbour[1] == current_pos[1]:	# same direction
				new_score += 1
			else:
				new_score += 100
			

			queue.append({
				"path": state["path"] + [neighbour],
				"score": new_score,
				})

		if k % 5000 == 0:
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


def draw(canvas: List, current_point: List, close_list: List, open_list: List, neighbours: List, start: Tuple, end: Tuple) -> None:
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
		x, y = point["path"][-1][0]  # Extract the position from the last step in the path
		if point["path"][-1] in neighbours:
			colour = dark_blue
		elif point["path"][-1] in current_path:
			colour = light_cyan
		else:
			colour = pure_red
		canvas[y][x] = colour + "█" + reset_colour

	# Colour close list
	for point in close_list:
		x, y = point[0]  # Extract the position
		if (x, y) == current_point["path"][-1][0]:  # Match the current point
			colour = orange
		elif point in current_path:
			colour = light_cyan
		else:
			colour = light_green
		canvas[y][x] = colour + "█" + reset_colour

	# Colour start and end
	canvas[start[0][1]][start[0][0]] = dark_cyan + "S" + reset_colour
	canvas[end[1]][end[0]] = dark_cyan + "E" + reset_colour

	# Print the canvas
	for row in canvas:
		print(" ".join(row))

	# Wait and clear output
	time.sleep(0.01)
	print("\033[1A" * len(canvas), end="\x1b[2K")


def draw_completed_path(canvas, path, start, end):
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
		pos = step[0]  # Extract position (x, y)
		x, y = pos
		if (x, y) == start[0]:
			continue  # Skip the start position
		if (x, y) == end:
			continue  # Skip the end position
		visual_canvas[y][x] = cyan_back + "█" + reset_colour

	# Highlight start and end positions
	visual_canvas[start[0][1]][start[0][0]] = dark_cyan + "S" + reset_colour
	visual_canvas[end[1]][end[0]] = light_green + "E" + reset_colour

	# Print the canvas
	for row in visual_canvas:
		print(" ".join(row))


def score_path(path: list) -> int:
	print(Counter([p[1] for p in path]))

	score = 0

	for i in range(1, len(path)):
		if path[i - 1][1] == path[i][1]:
			score += 1
		else:
			score += 1000
	return score


def score_paths(paths):
	scores = [score_path(path) for path in paths]
	print(scores)
	return scores


def find_best_paths(paths, scores):
	best_paths = []

	best = min(scores)
	for path, score in zip(paths, scores):
		if score == best:
			best_paths.append(path)

	return best_paths


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [list(line.strip()) for line in f]

	start = find_start(lines)
	end = find_end(lines)

	complete_path = pathfind(lines, start, end)

	print()

	all_visited = sum([p for p in complete_path], [])
	draw_completed_path(lines, all_visited, start, end)

	scores = score_paths(complete_path)
	print(f"Part I: {min(scores)}")

	best_paths = find_best_paths(complete_path, scores)
	print(best_paths)

	all_best_visited = sum([p for p in best_paths], [])
	draw_completed_path(lines, all_best_visited, start, end)
	
	all_best_visited = [p[0] for p in all_best_visited]
	print(f"Part II: {len(set(all_best_visited))}")


if __name__ == "__main__":
	main()
