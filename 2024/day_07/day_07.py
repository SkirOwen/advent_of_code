from __future__ import annotations

import itertools as it
import operator as op


def operation(nbr1: int, nbr2: int, operand: str) -> int:
	if operand == "*":
		return op.mul(nbr1, nbr2)
	if operand == "+":
		return op.add(nbr1, nbr2)
	if operand == "c":
		return int(str(nbr1) + str(nbr2))


def test_operators(nbrs: list[int], result: int, ops: str) -> int:
	valid_comb = 0
	operators_comb = it.product(ops, repeat=len(nbrs)-1)

	for operators in operators_comb:
		tot = 0
		prev_nbr = nbrs[0]

		for op_str, nbr in zip(operators, nbrs[1:]):
			tot = operation(prev_nbr, nbr, op_str)
			prev_nbr = tot

		if tot == result:
			valid_comb += 1

	return valid_comb


def evaluate_equations(equations: list, ops: str) -> int:
	tot = 0
	for equation in equations:
		result, nbrs = equation

		valid_comb = test_operators(nbrs, result, ops)

		if valid_comb:
			tot += result
	return tot


def parse(lines: list) -> list:
	eq = []

	for line in lines:
		lh, rh = line.split(":")
		rh = tuple(map(int, rh.split()))
		eq.append((int(lh), rh))
	return eq


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	equations = parse(lines)
	result1 = evaluate_equations(equations, ops="*+")

	print(f"Part I: {result1}")

	result2 = evaluate_equations(equations, ops="*+c")

	print(f"Part II: {result2}")


if __name__ == "__main__":
	main()
