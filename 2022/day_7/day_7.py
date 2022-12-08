from typing import List, Dict


def sum_in_folder():
	pass


def is_command(split_line: List) -> bool:
	return split_line[0] == "$"


def group_by_cmd(lines: List) -> List:
	grp = []
	cmd_idx = -1	# -1 to start at 0 with the first command added

	for line in lines:
		line = line.split()

		if is_command(line):
			cmd_idx += 1
			grp.append([line])
		else:
			grp[cmd_idx].append(line)
	return grp


def tree_files_in_folder(command_grp: List, verbose: bool = False) -> Dict:
	tree = {}
	r = 0
	full_path = []

	for v in command_grp:
		cmd = v[0]
		tab = "\t"

		if cmd[1] == "cd":
			directory = cmd[2]
			
			if directory ==  "..":
				full_path.pop()
				r -= 1
			elif directory != "/":
				if verbose:
					print(f"{tab * r}{directory}")

				full_path.append(directory)
				tree[" ".join(map(str, full_path))] = []
				r += 1
				
			else:
				full_path.append(directory)
				tree[" ".join(map(str, full_path))] = []

				if verbose:
					print("/")

		if cmd[1] == "ls":
			if verbose:
				for f in v[1:]:
					print(f"{tab * r}{f}")

			tree[" ".join(map(str, full_path))].extend(v[1:])
				# print(f"==={tree[directory]}")

	return tree


def get_dir_size(size_tree: Dict, tree: Dict, current_dir: str) -> int:
	for v in tree[current_dir]:
		if v[0] == "dir":
			nested_dir = f"{current_dir} {v[1]}"
			size_tree[current_dir] += get_dir_size(size_tree, tree, nested_dir)

		else:
			size_tree[current_dir] += int(v[0])
	return size_tree[current_dir]


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readlines()

	cmd_grp = group_by_cmd(lines)

	# for v in cmd_grp:
	# 	print(v)

	tree = tree_files_in_folder(command_grp=cmd_grp, verbose=False)

	size_tree = dict.fromkeys(tree.keys(), 0)

	starting_dir = "/"
	get_dir_size(size_tree=size_tree, tree=tree, current_dir=starting_dir)
	
	sum_dir_above_100_000 = 0

	for key, val in size_tree.items():
		if val <= 100_000:
			sum_dir_above_100_000 += val

	print(sum_dir_above_100_000)

if __name__ == "__main__":
	main()