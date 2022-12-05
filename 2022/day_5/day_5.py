from collections import deque
from typing import List


def get_init_condition(initial_position: List):
	# the last line of initial_position is the index of the stacks, but has some formating
	# split() it to get only the numbers, and taking the last one to get the total amount of stack
	nbr_of_stack = int(initial_position[-1].split()[-1])
	list_of_stack = [[] for i in range(nbr_of_stack)]

	print(list_of_stack) 

	for v in initial_position:
		ind_t = [i//10 for i in range(len(v))]
		ind_u = [i%10 for i in range(len(v))]
		print(*ind_t)
		print(*ind_u)
		print(*v)
		print(list(v[1::4]))
		print("="*35)



def instruction_parser(instructions: List) -> List:
	parsed_instruction = []
	for line in instructions:
		movement = line.split()[1::2]	# slicing to get the numbers in the line: "move n form p to q"

		parsed_instruction.append(
			list(map(int, movement))	# cast to int
			)

	return parsed_instruction


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readlines()
		
		instruction_line = lines.index("\n")
		initial_position = lines[:instruction_line]
		instructions = lines[instruction_line + 1:]

		parsed_instruction = instruction_parser(instructions)
		get_init_condition(initial_position)


if __name__ == '__main__':
	main()
