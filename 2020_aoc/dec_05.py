import numpy as np
import json

with open('dec_05_input.json', 'r') as f_read:
    all_seats = json.load(f_read)
# %%


def decode_row(seat_code):
    return seat_code.replace('F', '0').replace('B', '1')


def decode_col(seat_code):
    return seat_code.replace('L', '0').replace('R', '1')


def bin_to_num(s):
    return int(s, 2)


def split_seat_code(s):
    assert len(s) == 10
    return s[:7], s[7:]


def get_row_and_col_nums(s):
    row_s, col_s = split_seat_code(s)
    row_bin = decode_row(row_s)
    col_bin = decode_col(col_s)
    row_num = bin_to_num(row_bin)
    col_num = bin_to_num(col_bin)
    return row_num, col_num


def get_seat_id_from_s(s: str):
    assert len(s) == 10
    row_num, col_num = get_row_and_col_nums(s)
    return row_num * 8 + col_num


# %%
row_decoded = decode_row('BFFFBBF')
val = bin_to_num(row_decoded)
assert val == 70, f'{val} != 70'

assert get_seat_id_from_s('BFFFBBFRRR') == 567
# %%
results = []
for seat_code in all_seats:
    seat_id = get_seat_id_from_s(seat_code)
    results.append((seat_code, seat_id))

print(max(results, key=lambda t: t[1]))


# %% Find my seat
sparse = np.ndarray(shape=(128, 8), dtype=np.int8)
for item, seat_id in results:
    row, col = get_row_and_col_nums(item)
    print(row, col)
    sparse[row][col] = 1

with open('debug.txt', 'w') as f_writes:
    f_writes.write(str(sparse.tolist()))

print('now open in text editor and find the lone zero')
print('take the (row - 1) * 8 + (col - 1)')
