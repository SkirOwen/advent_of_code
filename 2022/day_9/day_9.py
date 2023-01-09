import operator as op

from typing import List, Tuple


def diagram_print(h_position: List, t_positions: List, height: int, width: int) -> None:
	grid = [["." for i in range(width + 1)] for j in range(height + 1)]
	grid[init_pos[1]][init_pos[0]] = "s"

	for i in range(len(t_positions)-1, -1, -1):
		x, y = t_positions[i][0], t_positions[i][1]
		print(x, y)
		grid[y][x] = i+1

	grid[h_position[1]][h_position[0]] = "H"
	
	for g in grid[::-1]:
		print(*g)
	print("\n")


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
		# print(amount_x, amount_y)

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


def update(instruction: Tuple, h_position: List, t_positions: List, hist_of_t: List) -> None:
	direction = instruction[0]
	amount = instruction[1]

	axis = direction[1]
	func = direction[0]

	for step in range(1, amount+1):
		
		h_position[axis] = func(h_position[axis], 1)
		prev_t = h_position

		for i, t_position in enumerate(t_positions):
			if check_update_t(prev_t, t_position):
				update_t(prev_t, t_position)

				if not (t_position in hist_of_t[i]):
					hist_of_t[i].append(t_position.copy())
			prev_t = t_position
		# diagram_print(h_position, t_positions, height, width)


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


def simulate_ropes(instructions: List, nbr_knots: int) -> List:
	amount_x = [i[1] if i[0][0] == op.add else -i[1] for i in instructions if i[0][1] == 0]
	amount_y = [i[1] if i[0][0] == op.add else -i[1] for i in instructions if i[0][1] == 1]
	global height
	global width
	height = abs(sum(amount_y))
	width = abs(sum(amount_x))
	print(height, width)

	global init_pos
	init_pos = [0, 0]

	h_position = [0, 0]
	t_positions = [[0, 0] for i in range(nbr_knots - 1)]
	hist_of_t = [[[0, 0]] for i in range(nbr_knots - 1)]

	# print(lines[0].split())
	# diagram_print(h_position, t_positions, height, width)

	for i, instruction in enumerate(instructions):
		# print(f"\n== {lines[i].split()} ==\n")
		# print(hist_of_t)
		update(instruction, h_position, t_positions, hist_of_t)
		# diagram_print(h_position, t_positions, height, width)

	return hist_of_t


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readlines()

	instructions = instruction_parser(lines)

	# Part One
	nbr_knots = 2
	hist_of_t = simulate_ropes(instructions, nbr_knots)
	print(len(hist_of_t[-1]))
	
	# Part Two
	nbr_knots = 10
	hist_of_t = simulate_ropes(instructions, nbr_knots)
	print(len(hist_of_t[-1]))

	# x_h = [i[0] for i in hist_of_t[0]]
	# y_h = [i[1] for i in hist_of_t[0]]
	# print(max(x_h), min(x_h))
	# print(max(y_h), min(y_h))

	# print("new", max(map(abs, x_h)), max(map(abs, y_h)))
	# print(max(hist_of_t[0]))

	# for instruction in instructions:
	# 	update(instruction, h_position, t_position)
	# 	print(h_position, t_position)


if __name__ == "__main__":
	main()
