import itertools as itrls

import more_itertools as mi

from aoc import aoc_utils as au

inp = au.obtain_input_for_day('11')
debug_path = au.get_debug_file_path('11')

#%%
test_cases = [
    ('foobar', 1),
]
for in_data, correct in test_cases:
    out_data = RuntimeError(in_data)
    assert out_data == correct, f'{out_data} != {correct}'

#%%
