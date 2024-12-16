from __future__ import annotations

from copy import deepcopy


def get_neighbours(grid: list, current_point: tuple[int, int]) -> List:
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

		if grid[y][x] - current_height != 1:
			continue

		neighbours.append(node_position)

	return neighbours


def trailfind(start: tuple[int, int], lines: list):

	init_state = {
		"pos": start,
		"parent": []
	}
	queue = [init_state]
	visited = []

	complete_path = []


	while queue:
		state = queue.pop(0)
		current_pos = state["pos"]

		if state not in visited:
			neighbours = get_neighbours(lines, current_pos)

			visited.append(state)
			x, y = current_pos

			# Path found
			if lines[y][x] == 9:
				state["parent"].append(current_pos)
				complete_path.append(state)


			for neighbour in neighbours:
				next_state = deepcopy(state)
				next_state["pos"] = neighbour
				next_state["parent"].append(current_pos)

				queue.append(next_state)

	return complete_path


def find_trailheads(lines: list[list[int]]) -> list[tuple[int, int]]:
	trailheads = []
	for y, line in enumerate(lines):
		for x, elevation in enumerate(line):
			if elevation == 0:
				trailheads.append((x, y))
	return trailheads


def find_different_summit(trails: list) -> set:
	unique_summit = set([trail["pos"] for trail in trails])
	return unique_summit


def rating_trailheads(trailheads: list, lines: list) -> int:
	rating = 0
	for trailhead in trailheads:
		trails = trailfind(trailhead, lines)
		rating += len(trails)

	return rating



def score_trailheads(trailheads: list, lines: list) -> int:
	score = 0
	for trailhead in trailheads:
		trails = trailfind(trailhead, lines)

		unique_summit = find_different_summit(trails)
		score += len(unique_summit)

	return score


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [list(map(int, line.strip())) for line in f]

	trailheads = find_trailheads(lines)

	score = score_trailheads(trailheads, lines)
	print(f"Part I: {score}")

	rating = rating_trailheads(trailheads, lines)
	print(f"Part II: {rating}")


if __name__ == "__main__":
	main()
