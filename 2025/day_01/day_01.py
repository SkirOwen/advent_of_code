from __future__ import annotations


def parse(lines: list) -> list[tuple[str, int]]:
	
	inst = []

	for line in lines:
		inst.append((line[0], int(line[1:])))

	return inst


def unlock(instructions: list, start: int = 50, use_method: bool = False):

	nbr_zeros = 0
	pos = start

	for instruction in instructions:
		direction = instruction[0]

		if use_method:
			if pos == 0 and direction == "L":
				nbr_zeros -= 1

			pos, pass_zero = turn(instruction, pos)


			nbr_zeros += pass_zero

			if pos == 0 and direction == "L":
				nbr_zeros += 1

		else:
			pos, pass_zero = turn(instruction, pos)
			if pos == 0:
				nbr_zeros += 1

	return nbr_zeros



def turn(instruction: tuple, start: int) -> int:
	direction = instruction[0]
	nbr = instruction[1]

	pos = start

	if direction == "R":
		pos += nbr
	else:
		pos -= nbr


	(pass_zero, end) = divmod(pos, 100)
	pass_zero = abs(pass_zero)


	return end, pass_zero


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	instructions = parse(lines)

	# print(instructions)

	nbr_zeros = unlock(instructions)
	print(nbr_zeros)

	print("----")

	nbr_zeros_method = unlock(instructions, use_method=True)
	print(nbr_zeros_method)


if __name__ == "__main__":
	main()
