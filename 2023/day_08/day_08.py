from __future__ import annotations

import math

from itertools import cycle


def parse_map(lines: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:

	instructions = lines[0]

	network = dict()
	for line in lines[2:]:
		node, edge = line.split(" = ")
		edge = tuple(edge.strip("()").split(", "))
		network[node] = edge

	return instructions, network


def follow_map(instructions: str, network: dict, start: str = "AAA", end: str = "ZZZ") -> list:
	current_node = start
	path = []

	for instruction in cycle(instructions):
		print(current_node)
		if current_node == end:
			break

		if instruction == "R":
			direction = 1
		else:
			direction = 0

		path.append(current_node)
		current_node = network[current_node][direction]

	return path


def follow_ghost_map(instructions: str, network: dict, start: str = "A", end: str = "Z") -> list:
	all_paths_len = []
	
	current_nodes = [node for node in network.keys() if node[-1] == start]

	for current_node in current_nodes:
		path = []
		for instruction in cycle(instructions):
			if current_node[-1] == end:
				break

			if instruction == "R":
				direction = 1
			else:
				direction = 0

			path.append(current_node)
			current_node = network[current_node][direction]

		all_paths_len.append(len(path))

	return all_paths_len


def graph(network):
	import networkx as nx
	import matplotlib.pyplot as plt
	from pyvis.network import Network

	G = nx.Graph(network)
	# options = {
    # "font_size": 5,
    # "node_size": 100,
    # "node_color": "white",
    # "edgecolors": "black",
    # "linewidths": 0.5,
    # "width": 1,
	# }
	# nx.draw_networkx(G, **options)
	net = Network()
	net.show_buttons() # Show part 3 in the plot (optional)
	net.from_nx(G) # Create directly from nx graph
	net.show('test.html', notebook=False)


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	instructions, network = parse_map(lines)

	path = follow_map(instructions, network)
	print(f"Part I: {len(path)}")

	starts = [node for node in network.keys() if node[-1] == "A"]
	print(starts)
	print([network[s] for s in starts])
	end = [node for node in network.keys() if node[-1] == "Z"]
	print(end)
	print([network[s] for s in end])
	
	ghost_path = follow_ghost_map(instructions, network)
	print(f"Part II: {math.lcm(*ghost_path)}")


if __name__ == "__main__":
	main()
