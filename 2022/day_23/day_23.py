from time import sleep


def line_parser(lines: list) -> list:
	elves = []
	for y, line in enumerate(lines, start=1):
		for x, c in enumerate(line, start=1):
			if c == "#":
				elves.append(complex(x, y))
	return elves


def next_round(elves: list, direction: list) -> list:
	potential_elves = []

	# Get potential position
	for elf in elves:
		# if all([(elf + v) not in elves for d in direction for v in d]):
		around_free = (
			(elf + direction[0][0] not in elves) and 
			(elf + direction[0][1] not in elves) and 
			(elf + direction[0][2] not in elves) and
			(elf + direction[1][0] not in elves) and 
			(elf + direction[1][1] not in elves) and 
			(elf + direction[1][2] not in elves) and
			(elf + direction[2][0] not in elves) and 
			(elf + direction[2][1] not in elves) and 
			(elf + direction[2][2] not in elves) and
			(elf + direction[3][0] not in elves) and 
			(elf + direction[3][1] not in elves) and 
			(elf + direction[3][2] not in elves)
		)
		if around_free:
			potential_elves.append(elf)
			continue

		can_move = False
		for d in direction:
			if (elf + d[0] not in elves) and (elf + d[1] not in elves) and (elf + d[2] not in elves):
				potential_elves.append(elf + d[1])
				can_move = True
				break

		if not can_move:
			potential_elves.append(elf)

	new_elves = []
	# Check if postion are clashing
	for elf, po_elf in zip(elves, potential_elves):
		if potential_elves.count(po_elf) == 1:
			new_elves.append(po_elf)
		else:
			new_elves.append(elf)

	# print(potential_elves)
	# print(new_elves)
	return new_elves


def simulate(elves: list, nbr_round: int = 10, drawing: bool = False) -> list:
	direction = [
		[complex(-1, -1), complex(0, -1), complex(1, -1)],
		[complex(-1, 1) , complex(0, 1) , complex(1, 1)],
		[complex(-1, -1), complex(-1, 0), complex(-1, 1)],
		[complex(1, -1) , complex(1, 0) , complex(1, 1)],
	]
	
	for i, r in enumerate(range(nbr_round), start=1):
		new_elves = next_round(elves, direction)
		direction.append(direction.pop(0))

		print(f"== End of Round {i} ==")
		if drawing:
			draw(new_elves)
			print("")

		if all([n_elf in elves for n_elf in new_elves]):
			print(i)
			break
		else:
			elves = new_elves

	return elves


def draw(elves: list) -> None:
	y_val = [elf.imag for elf in elves]
	x_val = [elf.real for elf in elves]

	y_max = int(max(y_val))
	x_max = int(max(x_val))

	y_min = int(min(y_val))
	x_min = int(min(x_val))

	canvas = [["." for x in range(x_max + 2)] for y in range(y_max + 2)]
	
	for elf in elves:
		a, b = int(elf.real), int(elf.imag)
		a -= x_min
		b -= y_min
		canvas[b][a] = "#"

	for row in canvas:
		print(*row)

	# print("\033[1A" * (len(canvas)), end="\x1b[2K")
	# sleep(3)


def count_empty_tiles(elves: list) -> int:
	y_val = [elf.imag for elf in elves]
	x_val = [elf.real for elf in elves]

	y_max = int(max(y_val))
	x_max = int(max(x_val))

	y_min = int(min(y_val))
	x_min = int(min(x_val))

	width = x_max - x_min
	height = y_max - y_min

	rectangle_area = (width + 1) * (height + 1)

	return rectangle_area - len(elves)


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readlines()

	# print(lines)

	elves = line_parser(lines)

	print(" == Initial State ==")
	print("")
	# draw(elves)

	final_pos = simulate(elves, nbr_round=30, drawing=False)
	empty_tile = count_empty_tiles(final_pos)
	print("")
	print(empty_tile)


if __name__ == "__main__":
	main()
