from __future__ import annotations

import re

def parse_mul(lines: list) -> list:
	instructions = []
	for line in lines:
		inst = re.findall(
			r"mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)", 
			line)
		instructions.extend(inst)

	# print(instructions)
	return instructions


def eval_instruction(instructions: list, conditional: bool = False) -> int:
	total = 0
	calculate = True

	for instruction in instructions:
		if instruction[:3] != "mul":
			if conditional:
				if instruction == "do()":
					calculate = True
				else:
					calculate = False
		else:
			if calculate:
				lh, rh = instruction.split(",")

				lh = int(lh.split("(")[1])
				rh = int(rh.strip(")"))

				total += (lh * rh)

	return total


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	test_lines = ["xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"]

	instructions = parse_mul(lines)
	# print(instructions)
	result1 = eval_instruction(instructions)
	result2 = eval_instruction(instructions, conditional=True)


	print(f"Part I: {result1}")
	print(f"Part II: {result2}")


if __name__ == "__main__":
	main()
