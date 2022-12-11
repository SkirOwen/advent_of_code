from typing import List


def addx(value: int) -> None:
	noop()
	output.append(output[-1] + value)


def noop() -> None:
	output.append(output[-1])


def get_signal_strength(cycle: int, register: List) -> int:
	return cycle * output[cycle-1]


def render() -> None:
	screen = [["." for i in range(40)] for j in range(6)]

	for cycle_0, sprite_pos in enumerate(output[:-1]):
		line = cycle_0 // 40
		pixel = cycle_0 % 40

		sprite_mid = cycle_0	# cycle_0 is just there to make it easier to count the indexes
		sprite_start = (sprite_mid % 40) - 1
		sprite_end = (sprite_mid % 40) + 1

		if sprite_start <= sprite_pos <= sprite_end:
			screen[line][pixel] = "#"

	for line in screen:
		print(*line)


def parser(lines: List) -> List:
	instructions = []
	for line in lines:
		instructions.append(line.split())
	return instructions


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		instructions = []
		for line in f:
			instructions.append(line.split())

	global X, output
	X = 1
	# cycle is the index of output
	output = [X]
	op = ["init"]

	for instruction in instructions:
		if instruction[0] == "noop":
			op.append("noop")
			noop()
		elif instruction[0] == "addx":
			op.append("|")
			op.append(f"addx {instruction[1]}")
			addx(value=int(instruction[1]))

	# Part One
	signal_strength_time = [i for i in range(20, 221, 40)]

	s = 0
	for t in signal_strength_time:
		score = get_signal_strength(cycle=t, register=output)
		s += score
	print(s)

	# Part Two
	render()


if __name__ == "__main__":
	main()
