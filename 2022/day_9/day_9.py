def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readlines()

	print(lines)

if __name__ == "__main__":
	main()
