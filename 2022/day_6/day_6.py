from collections import deque
from itertools import islice
from typing import Tuple, Iterable


def sliding_window(iterable: Iterable, n: int) -> Tuple:
	# https://docs.python.org/3/library/itertools.html#itertools-recipes
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def find_marker(message: Iterable, len_of_packet: int) -> int:
	for i, v in enumerate(sliding_window(message, len_of_packet)):
		if len(set(v)) == len_of_packet:
			return i + len_of_packet
			

def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		line = f.readlines()[0].strip()

	# Part One
	print(f"Start-of-packet marker at: {find_marker(message=line, len_of_packet=4)}")

	# Part One
	print(f"Start-of-message marker at: {find_marker(message=line, len_of_packet=14)}")


if __name__ == '__main__':
	main()
