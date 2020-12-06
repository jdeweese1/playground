from copy import deepcopy
import pprint
from aoc import aoc_utils as au

tree_map = au.obtain_input_for_day('03')
annotated = [list(item) for item in deepcopy(tree_map)]
# %%


def reindex(x):
    return x % len(tree_map[0])


def get_obj_at(x, y, mark=True):
    # assert y < len(tree_map)
    # ipdb.set_trace()
    x = reindex(x)
    val_at_pos = tree_map[y][x]

    if mark:
        annotated[y][x] = 'X' if val_at_pos == '#' else 'O'
    return val_at_pos


assert get_obj_at(0, 0, mark=False) == '.'
assert get_obj_at(1, 1, mark=False) == '#'
assert get_obj_at(0, 32, mark=False) == '.'
assert get_obj_at(1, 33, mark=False) == '.'

row_index = 0
col_index = 0

moves_right = 1
moves_down = 2

tree_hits = []
while True:
    if get_obj_at(col_index, row_index) == '#':
        tree_hits.append((col_index, row_index, True))
    else:
        tree_hits.append((col_index, row_index, False))
    col_index += moves_right
    row_index += moves_down
    # if col_index >= len(tree_map):
    #     break
# %%

print(len(tree_hits))

# %%


aoc_utils.write_to_debug_file_path(
    '\n'.join(''.join(item) for item in annotated))

with open('hits.txt', 'w') as f_writes:
    f_writes.write(pprint.pformat(tree_hits))

print(len(list(filter(lambda t: t[2], tree_hits))))
