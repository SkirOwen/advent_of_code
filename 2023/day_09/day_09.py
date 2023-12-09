from __future__ import annotations

from itertools import pairwise


def find_zero(line):
	line = list(map(int, line))
	steps = [line]

	while True:
		step = []
		for n, next_n in pairwise(line):
			diff = next_n - n
			step.append(diff)
		print(step)
		line = step
		steps.append(step)
		if all([s == 0 for s in step]):
			break
	return steps


def add_next_value(steps):
	values = []
	last_step_value = 0
	
	for step, next_step in pairwise(steps[::-1]):
		last_next_step_value = next_step[-1]

		predicted_val = last_step_value + last_next_step_value

		values.append(predicted_val)
		last_step_value = predicted_val
	return values


def add_previous_value(steps):
	values = []
	last_step_value = 0
	
	for step, next_step in pairwise(steps[::-1]):
		last_next_step_value = next_step[0]

		predicted_val = - last_step_value + last_next_step_value

		values.append(predicted_val)
		last_step_value = predicted_val
	return values


def run_all_predictions(lines, end=True):
	pred = [] 
	for line in lines:
		steps = find_zero(line)
		print(steps)
		if end:
			values = add_next_value(steps)
		else:
			values = add_previous_value(steps)
			print("V", values)
		pred.append(values[-1])
	return pred


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip().split() for line in f]


	pred = run_all_predictions(lines)
	print(f"Part I: {sum(pred)}")

	pred_prev = run_all_predictions(lines, end=False)
	print(f"Part II: {sum(pred_prev)}")


if __name__ == "__main__":
	main()
