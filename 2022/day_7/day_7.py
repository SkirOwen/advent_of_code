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

	for v in command_grp:
		cmd = v[0]
		tab = "\t"

		if cmd[1] == "cd":
			directory = cmd[2]
			
			if directory ==  "..":
				r -= 1
			elif directory != "/":
				if verbose:
					print(f"{tab * r}{directory}")
				tree[directory] = []
				r += 1
			else:
				tree[directory] = []
				if verbose:
					print("/")

		if cmd[1] == "ls":
			if verbose:
				for f in v[1:]:
					print(f"{tab * r}{f}")

			tree[directory].extend(v[1:])
				# print(f"==={tree[directory]}")

	return tree

def get_dir_size(size_tree: Dict, tree: Dict, directory: str) -> Dict:
	

	for v in tree[directory]:
		if v[0] == "dir":
			size = get_dir_size(size_tree, tree, v[1])
		else:
			size = int(v[0])	
		size_tree[directory] += size

	return size_tree[directory]


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readlines()

	cmd_grp = group_by_cmd(lines)

	tree = tree_files_in_folder(command_grp=cmd_grp, verbose=True)

	size_tree = dict.fromkeys(tree.keys(), 0)
	get_dir_size(size_tree, tree, "/")

	# for key, val in tree.items():
	# 	for v in val:
	# 		if v[0] != "dir":
	# 			size_tree[key] += int(v[0])
	# 	print("")
	for v in tree["/"]:
		print(v[0])

	print(size_tree)


if __name__ == "__main__":
	main()