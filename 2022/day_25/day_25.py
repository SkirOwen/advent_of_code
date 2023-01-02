def get_digit(character: str) -> int:
	match character:
		case "=":
			return -2
		case "-":
			return -1
		case other:
			return int(character)


def get_symbol(nbr: int) -> str:
	match character:
		case -2:
			return "="
		case -1:
			return "-"
		case other:
			return str(character)


def dec2snafu(nbr: int) -> str:
	snafu = []
	while nbr:
		value = int(nbr % 5)

		if value == 4:
			value = "-"
			nbr += 5
		elif value == 3:
			value = "="
			nbr += 5

		snafu.append(value)
		nbr //= 5

	return "".join(str(s) for s in snafu[::-1])


def snafu2dec(nbr: str) -> int:
	reversed_nbr = nbr[::-1]
	
	total = 0
	for i, c in enumerate(reversed_nbr):
		n = get_digit(c)
		total += n*5**i

	return total


def main() -> None:
	filename = "input.txt"

	lines = []

	with open(filename, "r") as f:
		for line in f:
			lines.append(line.strip())

	# print(lines)
	dec = []
	for v in lines:
		dec.append(snafu2dec(v))

	bas = []
	inter = []
	for v in dec:
		a = dec2snafu(v)
		bas.append(a)
	
	print("SNAFU".rjust(10), "Decimal".rjust(10), "base 5".rjust(10))
	for s, d, b in zip(lines, dec, bas):
		print(s.rjust(10), str(d).rjust(10), str(b).rjust(10))

	print(sum(dec))
	print(dec2snafu(sum(dec)))


if __name__ == "__main__":
	main()
