from __future__ import annotations


def follow_instruction(instructions: list, initial_pos: list[int, int], use_aim: bool = False) -> tuple[int, int]:
	pos = initial_pos.copy()
	if use_aim:
		pos.append(0)

	for instruction in instructions:
		pos = move(pos, instruction, use_aim)
	return pos


def move(pos, instruction: tuple[str, int], use_aim: bool = False) -> tuple[int, int]:
	amount = int(instruction[1])
	if use_aim:
		h_pos, depth, aim = pos
	else:
		h_pos, depth = pos

	match instruction[0]:
		case "forward":
			h_pos += amount
			if use_aim:
				depth += aim * amount
		case "up":
			if use_aim:
				aim -= amount
			else:
				depth -= amount
		case "down":
			if use_aim:
				aim += amount
			else:
				depth += amount

	pos = [h_pos, depth]

	if use_aim:
		pos.append(aim)
	return pos


def main() -> None:
	filename = "input.txt"

	lines = []

	with open(filename, "r") as f:
		for line in f:
			lines.append(line.strip().split())

	print("Part 1")
	pos = follow_instruction(instructions=lines, initial_pos=[0, 0])
	print(pos)
	print(pos[0] * pos[1])

	print("\n")
	print("Part 2")
	pos = follow_instruction(instructions=lines, initial_pos=[0, 0], use_aim=True)
	print(pos)
	print(pos[0] * pos[1])


if __name__ == '__main__':
	main()