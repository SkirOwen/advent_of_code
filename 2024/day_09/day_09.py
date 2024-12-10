from __future__ import annotations


def parse(lines: list) -> list[int]:
	disk_map = lines[0]
	disk_map = list(map(int, list(disk_map)))
	return disk_map


def unpack_disk_map(disk_map):
	unpacked_map = []
	for i, f in enumerate(disk_map):
		idx = i // 2
		file_space = i % 2	# if 0 than is file, 1 if free-space
		
		if not file_space:
			unpacked_map.extend([idx] * f)
		else:
			unpacked_map.extend(["."] * f)

	return unpacked_map


def frag(unpacked_map):
	frag_map = []
	pop_idx = -1
	# reversed_map = unpack_map.reverse()

	for idx, f in enumerate(unpacked_map):

		if (pop_idx % len(unpacked_map)) < idx:
			frag_map.append(".")

		elif f != ".":
			frag_map.append(f)
		else:
			re_value = unpacked_map[pop_idx]
			while re_value == ".":
				pop_idx -= 1
				re_value = unpacked_map[pop_idx]

			frag_map.append(re_value)
			pop_idx -= 1

	return frag_map


def defrag(disk_map):
    free_space = []
    files = {}

    disk_id = 0
    position = 0

    for i in range(len(disk_map)):
        size = int(disk_map[i])

        if i % 2 == 0:
            files[disk_id] = (position, size)

            disk_id += 1
        else:
            if size > 0:
                free_space.append((position, size))

        position += size

    for disk_id in range(len(files) - 1, -1, -1):
        pos, size = files[disk_id]
        found = None

        for idx, (start, length) in enumerate(free_space):
            if start >= pos:
                free_space = free_space[:idx]
                found = None
                break

            if size <= length:
                found = (idx, start, length)
                break

        if found:
            idx, start, length = found
            files[disk_id] = (start, size)

            if size == length:
                free_space.pop(idx)
            else:
                free_space[idx] = (start + size, length - size)

    return sum(
        disk_id * x
        for disk_id, (pos, size) in files.items()
        for x in range(pos, pos + size)
    )


def check_sum(defrag_map):
	tot = 0
	for i, f in enumerate(defrag_map):
		if f != ".":
			tot += i * f
	return tot


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	disk_map = parse(lines)

	unpacked_map = unpack_disk_map(disk_map)
	print(*unpacked_map)
	print()

	frag_map = frag(unpacked_map)
	print(*frag_map)

	result1 = check_sum(frag_map)
	print(f"Part I: {result1}")

	defrag_map = defrag(disk_map)


	# result2 = check_sum(defrag_map)
	print(f"Part II: {defrag_map}")


if __name__ == "__main__":
	main()
