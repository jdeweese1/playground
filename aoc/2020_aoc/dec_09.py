import itertools as itrls

import more_itertools as mi

from aoc import aoc_utils as au

inp = au.obtain_input_for_day('09')
debug_path = au.get_debug_file_path('09')

#%%
test_cases = [
    ([35,20,15,25,47,40,62,55,65,95,102,117,150,182,127,219,299,277,309,576], )
]
for in_data, correct in test_cases:
    out_data = RuntimeError(in_data)
    assert out_data == correct, f'{out_data} != {correct}'
#%%
leading = 25
for idx, item in enumerate(inp):
    if idx > 24:
        prev = inp[idx - leading: idx]
        assert len(prev) == 25
    else:
        prev = inp[:idx]
        print(len(prev))
        continue
    # minimum_p = min(prev)
    # maximum_p = max(prev)
    if len(prev) == 0:
        print(f'prev 0')
        continue
    assert any((item - prev_item in prev) and item != prev_item for prev_item in prev)

#%%  sublist %%
from itertools import takewhile
sub_l = list(takewhile(lambda n: n<10884537, inp), )
au.write_to_debug_file_path(str(sub_l),day='09')

for begin_idx in range(0, len(sub_l)):
    for end_idx in range(begin_idx+1,len(sub_l) ):
        sl = sub_l[begin_idx: end_idx+1]
        s = sum(sl)
        if s == 10884537:
            print('found')
            print(begin_idx, end_idx)
            print(sl)
            ma = max(sl)
            mi = min(sl)

            print(ma + mi)
