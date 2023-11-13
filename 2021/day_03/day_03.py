from __future__ import annotations


def get_gamma(lst_nbr: list) -> str:
	gamma = []

	nbr_size = len(lst_nbr[0])
	for i in range(nbr_size):
		ones = count_ones_col(i, lst_nbr)
		gamma.append(ones)

	gamma = ''.join(str(i) for i in gamma)
	return gamma


def get_epsilon(gamma: str) -> str:
	# flipping the bit by XORing 
	return ''.join('1' if bit == '0' else '0' for bit in gamma)


def count_ones_col(col_idx: int, lst_nbr: list) -> int:
	ones = 0
	zeros = 0
	size = len(lst_nbr)

	for nbr in lst_nbr:
		if nbr[col_idx] == "1":
			ones += 1
		else:
			zeros += 1

	if ones > zeros:
		value = 1
	else:
		value = 0
	print(f"{col_idx}: {ones}, {zeros}, {value}, {size // 2}")
	return value


def main() -> None:
	filename = "input.txt"

	lines = []

	with open(filename, "r") as f:
		for line in f:
			lines.append(line.strip())

	print(len(lines))

	gamma = get_gamma(lines)
	print(int(gamma, 2))
	print(gamma)

	epsilon = get_epsilon(gamma)
	
	print(int(epsilon, 2))
	print(f"{epsilon = }")

	print(int(gamma, 2) * int(epsilon, 2))


if __name__ == '__main__':
	main()
