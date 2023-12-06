with open("input.txt", "r") as file:
    data = file.read()
    seed_inputs, *data_blocks = data.split("\n\n")

seed_inputs = list(map(int, seed_inputs.split(":")[1].split()))
seeds = []

for i in range(0, len(seed_inputs), 2):
    seeds.append([seed_inputs[i], seed_inputs[i] + seed_inputs[i + 1]])

for data_block in data_blocks:
    ranges_list = []
    for line in data_block.splitlines()[1:]:
        ranges_list.append(list(map(int, line.split())))

    new_seeds = []

    while len(seeds) > 0:
        print("s", seeds)
        print(len(seeds))
        start, end = seeds.pop()

        for destination, source, length in ranges_list:
            overlap_start = max(start, source)
            overlap_end = min(end, source + length)
            print(f"{overlap_start = }")
            print(f"{overlap_end = }")
            print(overlap_start< overlap_end)

            if overlap_start < overlap_end:
                # print(overlap_start, start)
                # print(overlap_end, end)
                new_seeds.append(
                    [overlap_start - source + destination, overlap_end - source + destination])
                if overlap_start > start:
                    print("a")
                    seeds.append([start, overlap_start])
                if overlap_end < end:
                    print("b")
                    seeds.append([overlap_end, end])
                break
        else:
            new_seeds.append([start, end])
        print("target", new_seeds)

    seeds = new_seeds

ans = min(seeds)[0]
print(ans)