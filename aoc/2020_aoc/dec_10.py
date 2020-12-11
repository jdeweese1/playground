import itertools as itrls
from collections import Counter
import more_itertools as mi

from aoc import aoc_utils as au

inp = au.obtain_input_for_day('10')
debug_path = au.get_debug_file_path('10')
# %%
jolt_counter = Counter(inp)
spread = 3
# au.write_to_debug_file_path(str(sorted(inp)), '10')

# %%
device_joltage = max(inp) + 3


def get_jolt_jump_dict(inp):
    jolt_jump = {}
    running_jolts = 0
    sorted_jolts = sorted(jolt_counter.items(), key=lambda item: item[0])
    for jolt_val, num in sorted_jolts:
        if num != 1:
            return False, {}
        # print(running_jolts, jolt_val)
        jump = jolt_val - running_jolts
        if jump > 3:
            return False, {}
        if jump not in jolt_jump.keys():
            jolt_jump[jump] = 0
        jolt_jump[jump] += 1
        running_jolts = jolt_val
    return True, jolt_jump


b, res = get_jolt_jump_dict(inp)
res[3] += 1  # Account for jolt jump into device
print(res[1] * res[3])

#%%
test_cases = [
    ('foobar', 1),
]
for in_data, correct in test_cases:
    out_data = RuntimeError(in_data)
    assert out_data == correct, f'{out_data} != {correct}'

#%%
