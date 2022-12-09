from typing import List


def instruction_parser(instructions: List) -> List:
	parsed_instruction = []
	for line in instructions:
		instr = line.split()
		parsed_instruction.append((instr[0], int(instr[1])))
	return parsed_instruction


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readlines()

	instructions = instruction_parser(lines)
	starting_position = (0, 0)
	print(instructions) 


if __name__ == "__main__":
	main()
