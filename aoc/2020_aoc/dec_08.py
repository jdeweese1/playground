from aoc import aoc_utils as au

SUCCESS = 'success'
AOB = 'OUT OF BOUNDS'
LOOP_DETECTED = 'inf_loop_detected'

inp = au.obtain_input_for_day('08')
debug_path = au.get_debug_file_path('08')

# %%
test_cases = [
]
for in_data, correct in test_cases:
    out_data = RuntimeError(in_data)
    assert out_data == correct, f'{out_data} != {correct}'
    # %%


def run_program(inp: list):
    accum = 0
    last_instr_idx = len(inp) - 1
    instruct_ptr = 0
    idxes_and_vals = list(enumerate(inp))
    instruction_lines_ran = set()
    try:
        while True:
            item = idxes_and_vals[instruct_ptr]
            idx, (instruct, sign, un_v) = item
            if idx in instruction_lines_ran:
                return LOOP_DETECTED, accum
            if sign == '+':
                mult = 1
            else:
                mult = -1

            value = un_v * mult
            instruction_lines_ran.add(idx)
            if instruct == 'jmp':
                instruct_ptr += value
            elif instruct == 'nop':
                if last_instr_idx == instruct_ptr:
                    break
                instruct_ptr += 1
                continue
            elif instruct == 'acc':
                accum += value
                if last_instr_idx == instruct_ptr:
                    break
                instruct_ptr += 1
            # if instruct_ptr == len(index)
    except IndexError:
        return f'{AOB} AT LN {instruct_ptr}', accum
    return SUCCESS, accum


print(run_program(inp))
#1475
# %%
test_data = [
    ["nop", "+", 0],
    ["acc", "+", 1],
    ["jmp", "+", 4],
    ["acc", "+", 3],
    ["jmp", "-", 3],
    ["acc", "-", 99],
    ["acc", "+", 1],
    ["nop", "-", 4],
    ["acc", "+", 6]
]
test_ret = run_program(test_data)
assert test_ret == (SUCCESS, 8)
print(test_ret)

# %%
broken_data = [
    ["nop", "+", 0],
    ["acc", "+", 1],
    ["jmp", "+", 4],
    ["acc", "+", 3],
    ["jmp", "-", 3],
    ["acc", "-", 99],
    ["acc", "+", 1],
    ["jmp", "-", 4],
    ["acc", "+", 6]
]

broken_ret = run_program(broken_data)
assert broken_ret == (LOOP_DETECTED, 5)
print(broken_ret)


# %%
all_jmp_noops = [op for op in list(
    enumerate(inp)) if op[1][0] in ('jmp', 'nop')]
rets = []
for candidate_to_swap in all_jmp_noops:
    candidate_swap_index, (instr, sign, un_v) = candidate_to_swap

    new_inst = 'jmp' if instr == 'nop' else 'nop'

    new_p = au.obtain_input_for_day('08')
    new_p[candidate_swap_index] = (new_inst, sign, un_v)
    ret_val, accum = run_program(new_p)

    rets.append((candidate_swap_index, ret_val, accum))

    if SUCCESS in ret_val or AOB in ret_val:
        print(SUCCESS)
        print(ret_val)
        print(accum)
        break

# 635
