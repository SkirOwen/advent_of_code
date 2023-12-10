from __future__ import annotations
import numpy as np


def get_start(pipes):
	for b, pipe in enumerate(pipes):
		if "S" in pipe:
			a = pipe.index("S")
			return a, b


def get_neighbours(node, pipes, previous):
	neighbours = []
	a, b = node
	ap, bp = previous
	current = pipes[b][a]

	horizontal = "─"
	vertical = "│"
	up_left = "┌"
	up_right = "┐"
	down_left = "└"
	down_right = "┘"

	if current == "S":
		return [(a-1, b)]

	if current == horizontal:
		neighbours.append((a-1, b))
		neighbours.append((a+1, b))

	if current == vertical:
		neighbours.append((a, b-1))
		neighbours.append((a, b+1))

	if current == up_left:
		neighbours.append((a+1, b))
		neighbours.append((a, b+1))

	if current == up_right:
		neighbours.append((a-1, b))
		neighbours.append((a, b+1))

	if current == down_left:
		neighbours.append((a+1, b))
		neighbours.append((a, b-1))

	if current == down_right:
		neighbours.append((a-1, b))
		neighbours.append((a, b-1))

	return neighbours


def draw(visited, pipes, start):
	for b, pipe in enumerate(pipes):
		for a, p in enumerate(pipe):
			if (a, b) == start:
				print("\033[0;36m" + p + "\033[0m", end="")
			elif (a, b) in visited:
				print("\033[0;31m" + p + "\033[0m", end="")
			else:
				print(p, end="")
		print("")
	# print("\033[1A" * len(pipes), end="\x1b[2K")


def get_loop(pipes):
	start = get_start(pipes)
	node = start
	queue = [start]
	visited = []
	previous = start

	while len(queue) != 0:
		node = queue.pop()
		# draw(visited, pipes)
		neighbours = get_neighbours(node, pipes, previous)
		# print(neighbours)

		visited.append(node)
		for n in neighbours:
			if not n in visited:
				queue.append(n)
		previous = node

	return visited


def get_enclosed(visited, pipes):
	enclosed = []
	for b, pipe in enumerate(pipes):
		count = 0
		for a, p in enumerate(pipe):
			if ((a, b) in visited):
				if (pipes[b][a] in ["│", "┌", "┐"]):
					count += 1
			elif count % 2 == 1:
				enclosed.append((a,b))
	return enclosed


def replace_s(pipes, visited):
	a, b = get_start(pipes)
	next_pipe = visited[1] 
	prev_pipe = visited[-1]

	up = (a    , b - 1)
	le = (a - 1, b    )
	ri = (a + 1, b    )
	do = (a    , b + 1)

	not_loop = [up, le, ri, do]
	not_loop.remove(next_pipe)
	not_loop.remove(prev_pipe)

	if up in not_loop and do in not_loop:
		s_symbol = "─"

	if do in not_loop and ri in not_loop:
		s_symbol = "│"

	if ri in not_loop and up in not_loop:
		s_symbol = "┌"

	if up in not_loop and le in not_loop:
		s_symbol = "┐"

	if le in not_loop and do in not_loop:
		s_symbol = "└"

	if le in not_loop and ri in not_loop:
		s_symbol = "┘"

	pipes[b][a] = s_symbol
	return pipes


def get_map(lines):
	pipes = []
	for line in lines:
		pipes.append(list(line.translate(str.maketrans("-|F7LJ", "─│┌┐└┘"))))
	return pipes


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	pipes = get_map(lines)
	start = get_start(pipes)

	visited = get_loop(pipes)
	print(visited)
	print(f"Part I: {len(visited) / 2}")

	pipes_s = replace_s(pipes, visited)
	enclosed = get_enclosed(visited, pipes_s)
	draw(enclosed, pipes, start)
	print(f"Part II: {len(enclosed)}")
	print(start)


if __name__ == "__main__":
	main()
