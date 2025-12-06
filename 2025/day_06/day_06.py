from __future__ import annotations

import math


def parse(lines: list[str], vertical: bool = False) -> tuple[list[list[int]], list[str]]:

	size = len(lines)
	numbers = []
	operand = lines[-1].split()

	if not vertical:
		for i, line in enumerate(lines[:-1]):
			temp_line = line.split()
			numbers.append(list(map(int, temp_line)))

		numbers_T = [
			[
				numbers[i][j] for i in range(len(numbers))
			] for j in range(len(numbers[0]))
		]

	else:
		vertical_nbr = [[] for i in range(len(lines[0]))]

		for i, line in enumerate(lines[:-1]):
			for j, char in reversed(list(enumerate(line))):
				if char == " ":
					pass
				else:
					vertical_nbr[j].append(int(char))

		parsed_vertical = []
		column = []

		for v_n in vertical_nbr:

			if len(v_n) == 0:
				parsed_vertical.append(column)
				column = []
			else:
				nbr = 0
				for i, char in enumerate(v_n):
					nbr += char * 10 ** (len(v_n) - i - 1)

				column.append(nbr)  
		parsed_vertical.append(column)

		numbers_T = parsed_vertical

	return numbers_T, operand


def calculate(numbers: list[list[int]], operand: list[str]) -> int:
	total = 0

	for nbrs, ope in zip(numbers, operand):

		if ope == "+":
			total += sum(nbrs)
		elif ope == "*":
			total += math.prod(nbrs)

	return total


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip("\n") for line in f]

	numbers, operand = parse(lines)
	total = calculate(numbers, operand)
	print(total)
	print("--")

	numbers_v, operand_v = parse(lines, vertical=True)
	total_v = calculate(numbers_v, operand_v)
	print(total_v)


if __name__ == "__main__":
	main()
