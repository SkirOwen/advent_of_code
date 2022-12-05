from collections import deque
from typing import List, Deque


def get_init_condition(initial_position: List) -> List[Deque]:
	# the last line of initial_position is the index of the stacks, but has some formating
	# split() it to get only the numbers, and taking the last one to get the total amount of stack
	nbr_of_stack = int(initial_position[-1].split()[-1])
	list_of_stack = [deque([]) for i in range(nbr_of_stack)]

	for v in initial_position[:-1]:
		stack_line = list(v[1::4])	# represent the horizontal line of the stack, as if reading a line
		for i, box in enumerate(stack_line):
			if box != " ":
				list_of_stack[i].appendleft(box)

	return list_of_stack



def instruction_parser(instructions: List) -> List:
	parsed_instruction = []
	for line in instructions:
		movement = line.split()[1::2]	# slicing to get the numbers in the line: "move n form p to q"

		parsed_instruction.append(
			list(map(int, movement))	# cast to int
			)

	return parsed_instruction


def move_box_9000(state: List, stack_id: int, amount: int, target: int) -> None:
	for v in range(amount):
		moving_box = state[stack_id].pop()
		state[target].append(moving_box)


def move_box_9001(state: List, stack_id: int, amount: int, target: int) -> None:
	moving_boxes = []
	for v in range(amount):
		moving_boxes.append(state[stack_id].pop())
	
	state[target].extend(reversed(moving_boxes))


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readlines()
		
		instruction_line = lines.index("\n")
		initial_position = lines[:instruction_line]
		instructions = lines[instruction_line + 1:]
		parsed_instruction = instruction_parser(instructions)
		
		# Part One
		print("==Part One==")
		state = get_init_condition(initial_position)

		for amount, stack_id, target in parsed_instruction:
			move_box_9000(
				state,
				stack_id=stack_id-1,
				amount=amount,
				target=target-1
				)

		for v in state:
			print(v[-1])

		# Part Two
		print("==Part Two==")
		state = get_init_condition(initial_position)

		for amount, stack_id, target in parsed_instruction:
			move_box_9001(
				state,
				stack_id=stack_id-1,
				amount=amount,
				target=target-1
				)

		for v in state:
			print(v[-1])


if __name__ == '__main__':
	main()
