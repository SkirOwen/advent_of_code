from __future__ import annotations


def get_gamma(lst_nbr: list) -> int:
	gamma = []

	nbr_size = len(lst_nbr[0])
	for i in range(nbr_size):
		ones = count_ones_col(i, lst_nbr)
		gamma.append(ones)

	gamma = ''.join(str(i) for i in gamma)
	return int(gamma, 2)


def get_epsilon(gamma: int) -> int:
	# flipping the bit by XORing 
	return gamma ^ int("1" * (len(bin(gamma)) - 2), 2)


def count_ones_col(col_idx: int, lst_nbr: list) -> int:
	ones = 0
	size = len(lst_nbr)

	for nbr in lst_nbr:
		if nbr[col_idx] == "1":
			ones += 1

	if ones >= size // 2:
		value = 1
	else:
		value = 0
	return value


def main() -> None:
	filename = "input.txt"

	lines = []

	with open(filename, "r") as f:
		for line in f:
			lines.append(line.strip())

	print(len(lines))

	gamma = get_gamma(lines)
	print(f"{gamma = }")
	print(bin(gamma))

	epsilon = get_epsilon(gamma)
	print(bin(epsilon))
	print(f"{epsilon = }")
	print(gamma * epsilon)


if __name__ == '__main__':
	main()
