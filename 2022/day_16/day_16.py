import re

from typing import List, Dict


class Path:
	def __init__(self, time: int, inital_valve: Dict) -> None:
		self.time = time
		self.visited = [inital_valve]
		self.pressure = 0

	def copy(self):
		new_path = Path(time=self.time, inital_valve=self.visited[0])
		new_path.visited = self.visited.copy()
		new_path.pressure = self.pressure

		return new_path

	def __repr__(self):
		return f"time: {self.time}, visited: {[valves for valves in self.visited]}, p: {self.pressure}"


def lines_parser(lines: str) -> Dict:
	valves = {}
	for line in lines:
		split_line = list(filter(None, re.split(r"[ \n,:=;]", line)))
		name = split_line[1]
		flow_rate = int(split_line[5])
		connections = split_line[10:]

		valves[name] = [flow_rate, connections, False]
	return valves


def get_adj_mat(valves: Dict) -> List:
	size = len(valves)
	adj_mat = [[0 for i in range(size)] for j in range(size)]
	key = {name: i for i, (name, _) in enumerate(valves.items())}
	
	for i, (k, v) in enumerate(valves.items()):
		for c in v[1]:
			row = key[c]
			adj_mat[i][row] += 1

	return adj_mat


def get_dis_mat(adj_mat: List) -> List:
	size = len(adj_mat)
	dis_mat = [[0 if i == j else 10000 for i in range(size)] for j in range(size)]
	
	for j in range(size):
		for i in range(size):
			if adj_mat[j][i] != 0:
				dis_mat[j][i] = 1

	for k in range(size):
		for i in range(size):
			for j in range(size):
				if dis_mat[i][j] > dis_mat[i][k] + dis_mat[k][j]:
					dis_mat[i][j] = dis_mat[i][k] + dis_mat[k][j]

	return dis_mat


def simulation(valves: List, total_time: int, all_path: bool = False) -> List:
	keys = {name: i for i, (name, _) in enumerate(valves.items())}
	start_valve = keys["AA"]

	adj = get_adj_mat(valves)
	dis_mat = get_dis_mat(adj)
		
	path = Path(time=0, inital_valve=start_valve)
	queue = [path]
	flows = [v[0] for _, v in valves.items()]
	valves_open = []

	complete_paths = []

	while queue:
		path = queue.pop(0)
		new = []
		possible_valves = [i for i, v in enumerate(valves.items()) if (i not in path.visited) and (v[1][0] != 0)]
		time_per_valve = [dis_mat[path.visited[-1]][c] + 1 for c in possible_valves]
		if all_path:
			complete_paths.append(path)

		for t, adj_node in zip(time_per_valve, possible_valves):
			if path.time + t >= total_time:
				continue
			extend_path = path.copy()
			extend_path.time += t
			extend_path.visited.append(adj_node)
			extend_path.pressure += (total_time - (path.time + t)) * flows[adj_node]
			
			new.append(extend_path)

		if new:
			# print(f"{new = }")
			queue.extend(new)
		else:
			if not all_path:
				complete_paths.append(path)

	return complete_paths


def simulation_elephants(valves: List) -> List:

	all_paths = simulation(valves, total_time=26, all_path=True)
	ranked_pressure_all_paths = sorted(all_paths, key=lambda v: v.pressure, reverse=True)
	max_pressure = 0

	j = 0
	for i, p in enumerate(ranked_pressure_all_paths):
		# remove the symmetry
		if i > j:
			continue
		worker_1 = set(p.visited[1:])
		for j, e in enumerate(ranked_pressure_all_paths[i+1:], start=i):
			if p.pressure + e.pressure <= max_pressure:
				break
			worker_2 = set(e.visited[1:])
			
			if len(worker_1 & worker_2) == 0:
				if p.pressure + e.pressure > max_pressure:
					max_pressure = p.pressure + e.pressure
	return max_pressure


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readlines()

	valves = lines_parser(lines)

	# Part One
	paths = simulation(valves, total_time=30)
	# print(paths)
	print(max([path.pressure for path in paths]))

	# Part Two
	elephant_pressure = simulation_elephants(valves)
	print(elephant_pressure)


if __name__ == "__main__":
	main()
