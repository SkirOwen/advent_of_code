import operator as op

from typing import List, Tuple


def check_update_t(h_position: List, t_position: List) -> bool:
	x_h, y_h = h_position

	x_diff = x_h - t_position[0]
	y_diff = y_h - t_position[1]
	return abs(x_diff) > 1 or abs(y_diff) > 1


def update_t(h_position: List, t_position: List) -> None:
	x_h, y_h = h_position
	x_t, y_t = t_position

	x_diff = x_h - x_t
	y_diff = y_h - y_t

	# print(x_diff, y_diff)

	if x_h != x_t and y_h != y_t:
		amount_x = x_diff // abs(x_diff)
		amount_y = y_diff // abs(y_diff)
		print(amount_x, amount_y)

		t_position[0] += amount_x
		t_position[1] += amount_y
		# print(t_position)
	else:
		# print("A")
		if y_diff > 1:
			# t moves up
			t_position[1] += 1
		elif y_diff < -1:
			# t moves down
			t_position[1] -= 1

		if x_diff > 1:
			# t moves right
			t_position[0] += 1
		elif x_diff < -1:
			# t moves left
			t_position[0] -= 1


def update(instruction: Tuple, h_position: List, t_position: List, hist_of_t: List) -> None:
	direction = instruction[0]
	amount = instruction[1]

	axis = direction[1]
	func = direction[0]

	for step in range(1, amount+1):
		h_position[axis] = func(h_position[axis], 1)

		if check_update_t(h_position, t_position):
			update_t(h_position, t_position)

			if not(t_position in hist_of_t):
				hist_of_t.append(t_position.copy())


def direction_parser(direction: str) -> Tuple:
	if direction == "U":
		return (op.add, 1)
	elif direction == "L":
		return (op.sub, 0)
	elif direction == "R":
		return (op.add, 0)
	else:	# i.e == "D"
		return (op.sub, 1)


def instruction_parser(instructions: List) -> List:
	parsed_instruction = []
	for line in instructions:
		instr = line.split()

		direction = instr[0]
		parsed_direction = direction_parser(direction)

		amount = int(instr[1])
		
		parsed_instruction.append((parsed_direction, amount))
	return parsed_instruction


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readlines()

	instructions = instruction_parser(lines)

	h_position = [0, 0]
	t_position = [0, 0]
	hist_of_t = [[0, 0]]

	# print(lines[0].split())

	for i, instruction in enumerate(instructions):
		print(f"\n== {lines[i].split()} ==\n")
		# print(hist_of_t)
		update(instruction, h_position, t_position, hist_of_t)

	print(len(hist_of_t))

	# for instruction in instructions:
	# 	update(instruction, h_position, t_position)
	# 	print(h_position, t_position)


if __name__ == "__main__":
	main()
