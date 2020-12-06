from aoc import aoc_utils

nums = aoc_utils.obtain_input_for_day('01')

# %%
for item in nums:
    for inner in nums:
        if item + inner == 2020:
            print('success!')
            print(f'{item}, {inner}')
            print(item * inner)


# %%
for i in nums:
    for j in nums:
        for k in nums:
            if i + j + k == 2020:
                print('success!')
                print(f'{i}, {j} {k}')
                print(i * j * k)
