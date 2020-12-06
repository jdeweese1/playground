# %% Find my seat
import numpy as np

from aoc import aoc_utils

all_seats = aoc_utils.obtain_input_for_day('05')
# %%


def decode_row(seat_code):
    return seat_code.replace('F', '0').replace('B', '1')


def decode_col(seat_code):
    return seat_code.replace('L', '0').replace('R', '1')


def bin_to_num(s):
    return int(s, 2)


def get_all_features_from_s(s: str):
    assert len(s) == 10
    row_s, col_s = s[:7], s[7:]

    row_bin, col_bin = decode_row(row_s), decode_col(col_s)
    row_num, col_num = bin_to_num(row_bin), bin_to_num(col_bin)
    seat_id = row_num * 8 + col_num
    return {
        'row_s': row_s,
        'col_s': col_s,
        'row_bin': row_bin,
        'col_bin': col_bin,
        'row_num': row_num,
        'col_num': col_num,
        'seat_id': seat_id,
    }


# %%
row_decoded = decode_row('BFFFBBF')
val = bin_to_num(row_decoded)
assert val == 70, f'{val} != 70'

assert get_all_features_from_s('BFFFBBFRRR')['seat_id'] == 567
assert get_all_features_from_s('FFFBBBFRRR')['seat_id'] == 119
assert get_all_features_from_s('BBFFBBFRLL')['seat_id'] == 820
# %%
results = []
for seat_code in all_seats:
    seat_id = get_all_features_from_s(seat_code)['seat_id']
    results.append((seat_code, seat_id))

print(max(results, key=lambda t: t[1]))


arr = np.ndarray(shape=(128, 8), dtype=np.int8)
for item, seat_id in results:
    feats = get_all_features_from_s(item)
    row = feats['row_num']
    col = feats['col_num']
    print(row, col)
    arr[row][col] = 1

aoc_utils.write_to_debug_file_path(str(arr.tolist()), '05')
