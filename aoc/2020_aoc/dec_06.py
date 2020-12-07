from collections import Counter
from typing import List, AnyStr

import more_itertools as mi

from aoc import aoc_utils as au

inp = au.obtain_input_for_day('06')
debug_path = au.get_debug_file_path('06')
# %%


def how_many_questions_anyone_answered(l: List[AnyStr]):
    c = 0
    for group in l:
        s = set(mi.flatten(group))
        c += len(s)
    return c


# %%
t = [
    ['abc', ],
    ['a', 'b', 'c', ],
    ['ab', 'ac', ],
    ['a', 'a', 'a', 'a', ],
    ['b']
]
test_cases = [
    (t, 11),
]
for in_data, correct in test_cases:
    out_data = how_many_questions_anyone_answered(in_data)
    assert out_data == correct, f'{out_data} != {correct}'

# %%
print(how_many_questions_anyone_answered(inp))
# %%


def how_many_questions_every_one_answers(l: List[AnyStr]):
    count = 0
    for group in l:
        freq_count = Counter(mi.flatten(group))
        num_all_answered = len(
            list(k for k in freq_count.keys() if freq_count[k] == len(group)))
        count += num_all_answered
    return count


res = how_many_questions_every_one_answers(t)
assert res == 6, f'{res} != {6}'

print(how_many_questions_every_one_answers(inp))
