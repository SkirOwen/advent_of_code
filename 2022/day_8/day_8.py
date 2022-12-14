from typing import List


def viewing_distance(tree: int, view_direction: List) -> int:
	for i, t in enumerate(view_direction, start=1):
		if t >= tree:
			return i
	return len(view_direction)


def score_tree(tree: int, directions: List) -> int:
	score = 1
	for view_direction in directions:
		score *= viewing_distance(tree, view_direction)
	return score


def grid_score_tree(grid: List) -> List:
	senic_score = [[0 for i in range(len(grid))] for j in range(len(grid))]
	grid_size = len(grid)

	for y in range(1, grid_size - 1):
		y_line = grid[y]
		for x in range(1, grid_size - 1):
			x_line = [i[x] for i in grid]

			up = x_line[:y]
			left = y_line[:x]
			right = y_line[x+1:]
			down = x_line[y+1:]

			tree = grid[y][x]

			# need to reverse the order of up and left to get the distance from the tree
			directions = [up[::-1], left[::-1], right, down]
			senic_score[y][x] = score_tree(tree, directions)

	return senic_score


def grid_visible_tree(grid: List) -> List:
	visible_tree = [[True for i in range(len(grid))] for j in range(len(grid))]
	grid_size = len(grid)

	for y in range(1, grid_size - 1):
		y_line = grid[y]
		for x in range(1, grid_size - 1):
			x_line = [i[x] for i in grid]

			up = x_line[:y]
			left = y_line[:x]
			right = y_line[x+1:]
			down = x_line[y+1:]

			tree = grid[y][x]

			if (tree <= max(up)) and (tree <= max(down)) and (tree <= max(left)) and (tree <= max(right)):
				visible_tree[y][x] = False

	return visible_tree


def main() -> None:
	filename = "input.txt"
	grid = []

	with open(filename, "r") as f:
		for line in f:
			grid.append(list(map(int, line.strip())))

	# Part One
	visible_tree = grid_visible_tree(grid)
	print(sum(map(sum, visible_tree)))

	# Part Two
	score_grid = grid_score_tree(grid)
	print(max(map(max, score_grid)))


if __name__ == "__main__":
	main()
