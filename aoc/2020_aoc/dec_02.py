from aoc import aoc_utils

rule_list = aoc_utils.obtain_input_for_day('02')

matches = []

for item in rule_list:
    occ_rule, letter, pw = item
    beg_occ, end_occ = occ_rule
    if beg_occ <= pw.count(letter) <= end_occ:
        matches.append(item)

print(len(matches))

# %%
matches = []
for item in rule_list:
    occ_rule, letter, pw = item
    beg_occ, end_occ = occ_rule
    pw = ' ' + pw
    # import ipdb; ipdb.set_trace()
    if pw[beg_occ].count(letter) + pw[end_occ].count(letter) == 1:
        matches.append(item)
print(len(matches))
