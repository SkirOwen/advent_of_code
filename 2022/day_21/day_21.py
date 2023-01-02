import operator as op
import collections

from itertools import islice
from typing import List, Dict, Callable


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def get_op(sign: str) -> Callable:
	match sign:
		case "+":
			return op.add
		case "-":
			return op.sub
		case "*":
			return op.mul
		case "/":
			return op.truediv


def find_invers_op(operation: Callable) -> Callable:
	match operation:
		case op.add:
			return op.sub
		case op.sub:
			return op.add
		case op.mul:
			return op.truediv
		case op.truediv:
			return op.mul


def line_parser(lines: List) -> Dict:
	monkeys = {} 
	for line in lines:
		split_line = line.split()

		monkey_id = split_line[0][:-1]
		if len(split_line) == 2:
			value = [int(split_line[1])]
		else:
			func = get_op(split_line[2])
			value = [split_line[1], split_line[3], func]

		monkeys[monkey_id] = value
	return monkeys


def calculate_monkey(monkeys, monkey_id) -> int:
	if type(monkeys[monkey_id][0]) == int or type(monkeys[monkey_id][0]) == float:
		return monkeys[monkey_id][0]
	elif len(monkeys[monkey_id]) == 1:
		val = calculate_monkey(monkeys, monkeys[monkey_id][0])
		return val
	else:
		nbr1 = calculate_monkey(monkeys, monkeys[monkey_id][0])
		nbr2 = calculate_monkey(monkeys, monkeys[monkey_id][1])
		value = monkeys[monkey_id][2](nbr1, nbr2)
		return value


def change_to_humn(monkeys: Dict) -> Dict:
	humn_instr = monkeys.copy()
	parents_humn = []

	monkey_id = "humn"
	parents_humn.append(monkey_id)

	while "root" not in parents_humn:
		for k, v in monkeys.items():
			if monkey_id in v:
				parents_humn.append(k)
				monkey_id = k

	# is the parents of "humn" to reverse the operation
	# until reaching "root"

	for key, moving in sliding_window(parents_humn, 2):
		a = monkeys[moving][0]
		b = monkeys[moving][1]
		# Careful order of op /!\, it got me the first time 
		from_right = b == key
		operation = monkeys[moving][2]

		match operation:
			case op.add:
				if from_right:
					humn_instr[key] = [moving, a, find_invers_op(operation)]
				else:
					humn_instr[key] = [moving, b, find_invers_op(operation)]

			case op.sub | op.truediv:
				if from_right:
					humn_instr[key] = [a, moving, operation]
				else:
					humn_instr[key] = [b, moving, find_invers_op(operation)]

			case op.mul:
				if from_right:
					humn_instr[key] = [moving, a, find_invers_op(operation)]
				else:
					humn_instr[key] = [moving, b, find_invers_op(operation)]


	# remove root and rename
	humn_instr.pop("root")
	for k, v in humn_instr.items():
		if "root" in v:
			nbr1 = humn_instr[k][0]
			nbr2 = humn_instr[k][1]
			humn_instr[k] = [
				nbr1 if nbr1 != "root" else nbr2
			]

	return humn_instr


def main() -> None:
	filename = "input.txt"

	# lines = []

	with open(filename, "r") as f:
		lines = f.readlines()

	# print(lines)
	monkeys = line_parser(lines)
	# print(monkeys)

	# Part One
	root_val = calculate_monkey(monkeys, monkey_id="root")
	print("root val:", int(root_val))

	# Part Two
	humn_instr = change_to_humn(monkeys)
	humn_val = calculate_monkey(humn_instr, monkey_id="humn")
	print("humn val:", int(humn_val))
	# 3093175982595

if __name__ == "__main__":
	main()
