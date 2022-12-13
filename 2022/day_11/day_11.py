import re
import operator as op

from functools import reduce
from heapq import nlargest
from typing import List


def get_monkey_business(monkey_1: int, monkey_2: int) -> int:
	return monkey_1 * monkey_2


def get_op_function(symbol: str, val: str) -> List:
	if val == "old":
		return [op.pow, 2]

	if symbol == "+":
		return [op.add, int(val)]
	elif symbol == "*":
		return [op.mul, int(val)]


def monkey_parser(lines: List) -> List:
	# monkeys = [
	# 	{	# monkey 0
	# 		"starting_items": [*ints]
	# 		"operation": [func, int]
	# 		"test": [int, if, else]
	# 	},
	# 	...
	# ]
	monkeys = []
	for line in lines:
		if line == "\n":	# removing the blank lines
			continue

		split_line = list(filter(None, re.split(r"[ \n,:]", line)))

		if split_line[0] == "Monkey":
			monkey_id = split_line[1]
			monkey = {}
		elif split_line[0] == "Starting":
			numbers = list(map(int, split_line[2:]))
			monkey["starting_item"] = numbers
		elif split_line[0] == "Operation":
			monkey["operation"] = get_op_function(split_line[-2], split_line[-1])
		elif split_line[0] == "Test":
			monkey["test"] = [int(split_line[-1])]

		elif split_line[1] == "true":
			monkey["test"].append(int(split_line[-1]))

		elif split_line[1] == "false":
			monkey["test"].append(int(split_line[-1]))

			monkeys.append(monkey)

	return monkeys


def monkeys_round(monkeys: List, inspection_level: List, worry_increase: bool) -> None:
	worry_div = reduce(op.mul, [m["test"][0] for m in monkeys])

	for monkey_id, monkey in enumerate(monkeys):
		# print(f"Monkey {monkey_id}:")

		for item in monkey["starting_item"]:
			inspection_level[monkey_id] += 1
			# print(f"\tMonkey inspects an item with a worry level of {item}.")
			# if monkey["operation"][0] == "pow":
			# 	worry = item
			# else:
			worry = monkey["operation"][0](item, monkey["operation"][1])
			# print(f"\t\tWorry level is op by {monkey['operation'][1]} to {worry}")
			if worry_increase:
				worry = worry // 3
				# print(f"\t\tMonkey gets bored with item. Worry level is divided by 3 to {worry}")

			else:
				worry = worry % worry_div 	# div by the prod of all the monke tests (no need for lcm as they are prime)

			if worry % monkey["test"][0] == 0:
				# print(f"\t\tCurrent worry level is not divisible by {monkey['test'][0]}.")
				# print(f"\t\tItem with worry level {worry} is thrown to monkey {monkey['test'][1]}.")
				monkeys[monkey["test"][1]]["starting_item"].append(worry)
			else:
				# print(f"\t\tCurrent worry level is divisible by {monkey['test'][0]}.")
				# print(f"\t\tItem with worry level {worry} is thrown to monkey {monkey['test'][2]}.")
				monkeys[monkey["test"][2]]["starting_item"].append(worry)
		
		monkey["starting_item"] = []


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readlines()

	# # Part One
	monkeys = monkey_parser(lines)
	inspection_level = [0 for i in range(len(monkeys))]
	worry_increase = True
	for i in range(20):
		monkeys_round(monkeys, inspection_level, worry_increase)

	top_two_monkeys = nlargest(2, inspection_level)
	print(get_monkey_business(top_two_monkeys[0], top_two_monkeys[1]))

	# Part Two
	monkeys = monkey_parser(lines)
	inspection_level = [0 for i in range(len(monkeys))]
	worry_increase = False
	for i in range(10_000):
		monkeys_round(monkeys, inspection_level, worry_increase)
		# print(*monkeys)

	top_two_monkeys = nlargest(2, inspection_level)
	print(get_monkey_business(top_two_monkeys[0], top_two_monkeys[1]))


if __name__ == "__main__":
	main()
