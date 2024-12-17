from __future__ import annotations

def parse_lines(lines: list[str]) -> tuple[dict, tuple[int, ...]]:
	register = lines[:3]
	instruction = lines[-1]

	reg = {
		"a": int(register[0].split(": ")[1]),
		"b": int(register[1].split(": ")[1]),
		"c": int(register[2].split(": ")[1]),
	}
	inst = tuple(map(int, instruction.split(": ")[1].split(",")))

	return reg, inst


def combo_oprand(operand: int, reg: dict) -> int:
	if operand <= 3:
		return operand

	elif operand == 4:
		return reg["a"]

	elif operand == 5:
		return reg["b"]

	elif operand == 6:
		return reg["c"]


def run_instruction(inst: tuple[int, ...], reg: dict, cntr: int):
	opcode, operand = inst[cntr: cntr+2]

	out = None
	# instruction:
	match opcode:
		case 0:		# adv
			num = reg["a"]
			den = 2 ** combo_oprand(operand, reg)
			reg["a"] = num // den

		case 1:		# bxl
			reg["b"] = reg["b"] ^ operand

		case 2:		# bst
			reg["b"] = combo_oprand(operand, reg) % 8

		case 3:		# jnz
			if reg["a"] != 0:
				return reg, operand, out

		case 4:		# bxc
			reg["b"] = reg["b"] ^ reg["c"]

		case 5:		# out
			out = combo_oprand(operand, reg) % 8
			# print(out, end=",")

		case 6:		# bdv
			num = reg["a"]
			den = 2 ** combo_oprand(operand, reg)
			reg["b"] = num // den

		case 7:		# cdv
			num = reg["a"]
			den = 2 ** combo_oprand(operand, reg)
			reg["c"] = num // den

	cntr += 2

	return reg, cntr, out


def run(inst, reg):
	out_put = []
	
	cntr = 0
	while cntr < len(inst):
		reg, cntr, out = run_instruction(inst, reg, cntr=cntr)
		
		if out is not None:
			out_put.append(out)
	return out_put


def search_quine(inst, reg):

	todo = [(list(inst), len(inst) - 1, 0, True, [])]
	
	while len(todo) > 0:
		inst, off, val, calc, added = todo.pop(0)

		if calc:
			for cur in range(8):
				new_val = (val << 3) + cur # reg a
				
				new_reg = reg.copy()
				new_reg["a"] = new_val

				out = run(inst, new_reg)

				if out == inst[off:]:
					if off == 0:
						return new_val

					todo.append((inst, off - 1, new_val, True, added + [cur]))
				else:
					todo.append((inst, off - 1, new_val, False, added + [cur]))
	return	None




def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	reg, inst = parse_lines(lines)

	out_put = run(inst, reg.copy())
	print("Part I:\n", ",".join(str(x) for x in out_put), "\n")

	a_quine = search_quine(inst, reg.copy())
	print("Part II:\nReg A value for quine:", a_quine)


if __name__ == "__main__":
	main()
