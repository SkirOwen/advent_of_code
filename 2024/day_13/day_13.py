from __future__ import annotations


def solver(A: list[list[int]], b: list[int]) -> tuple[float, float] | bool:
	det_a = A[0][0] * A[1][1] - A[1][0] * A[0][1]

	if not det_a:
		return False

	x = (A[1][1] * b[0] - A[0][1] * b[1]) / det_a
	y = (A[0][0] * b[1] - A[1][0] * b[0]) / det_a

	return (x, y)


def parse_arcade_machines(machines_lines: list[str]) -> list[list[int]]:
	machines_mtxs = []

	for idx, machine_l in enumerate(machines_lines):
		
		a_inst, b_inst, p_inst = machine_l
		a_inst = a_inst.split(": ")[1].split(", ")
		b_inst = b_inst.split(": ")[1].split(", ")
		p_inst = p_inst.split(": ")[1].split(", ")

		button = [
			[int(a_inst[0][2:]), int(b_inst[0][2:])],
			[int(a_inst[1][2:]), int(b_inst[1][2:])],
		]
		price = [
			int(p_inst[0][2:]),
			int(p_inst[1][2:]),
		]
		machines_mtxs.append([button, price])

	return machines_mtxs


def solve_machines(machines_mtxs: list[list[int]], limit_100: bool = True) -> int:
	tot = 0

	for (eq_a, eq_b) in machines_mtxs:
		if not limit_100:
			eq_b = [v + 10000000000000 for v in eq_b]

		sol = solver(eq_a, eq_b)
		
		a, b = sol

		if 0 <= a and 0 <= b and round(a, 3) == int(a) and round(b, 3) == int(b):
			if limit_100:
				if a <= 100 and b <= 100:
					tot += int(a * 3 + b)
			else:
				tot += int(a * 3 + b)

	return tot


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	machines_lines = [lines[i:i + 3] for i in range(0, len(lines), 4)]
	machines_mtxs = parse_arcade_machines(machines_lines)

	result1 = solve_machines(machines_mtxs, limit_100=True)
	print(f"Part I: {result1}")

	result2 = solve_machines(machines_mtxs, limit_100=False)
	print(f"Part II: {result2}")


if __name__ == "__main__":
	main()
