from itertools import cycle

from typing import List


def mix(coor: List, nbr_mix: int = 1, decryption_key: int = 1) -> List:
	coor = [(c * decryption_key) for c in coor]
	lst_index = [i for i in range(len(coor))]

	values = list(zip(coor, lst_index))

	for _ in range(nbr_mix):
		for i in range(len(coor)):
			idx = [v[1] for v in values]
			nbr = values.pop(idx.index(i))
			# print(nbr[0])
			if nbr[0] != -idx.index(i):
				idx_insert = (((idx.index(i) + nbr[0]) % (len(coor) - 1)))
				values.insert(idx_insert, nbr)
			else:
				# cant insert at -1, it will insert(-1, x) will put at -2
				# so uses append to fix at the nbr
				# mirror the problem
				values.append(nbr)

	return [v[0] for v in values]


def found_coord(mixed_line: List, stop_values: List) -> List:
	coord = []
	value_z = mixed_line.index(0)
	print(value_z)

	for v in stop_values:
		idx = (value_z + v) % (len(mixed_line))
		coord.append(mixed_line[idx])

	return coord


def main() -> None:
	filename = "input.txt"

	lines = []

	with open(filename, "r") as f:
		for line in f:
			# print(line.split())
			lines.append(int(line.split()[0]))

	# print(len(lines))
	# # print(lines)
	# Part One
	mixed_line = mix(lines)
	print(mixed_line)

	stop_values = [1000, 2000, 3000]
	coor = found_coord(mixed_line, stop_values)
	print(coor)
	print(sum(coor))
	# 1591

	# Part Two
	decryption_key = 811589153
	mixed_line = mix(lines, nbr_mix=10, decryption_key=decryption_key)
	stop_values = [1000, 2000, 3000]
	coor = found_coord(mixed_line, stop_values)
	print(coor)
	print(sum(coor))


if __name__ == "__main__":
	main()
