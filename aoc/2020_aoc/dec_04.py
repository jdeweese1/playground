# %%
import pprint
# %%
import re

from more_itertools import chunked

from aoc import aoc_utils as au

passports = au.obtain_input_for_day('04')
# %%
fields = ['byr',
          'iyr',
          'eyr',
          'hgt',
          'hcl',
          'ecl',
          'pid', ]


def contains_required_fields(pprt):
    return all(field in pprt for field in fields)


valids = []
for pprt in passports:
    if contains_required_fields(pprt):
        valids.append(pprt)

print(len(valids))


def height_valid(s):
    unit = s[-2:]
    height_pattern = re.compile('[0-9]+')
    match = height_pattern.findall(s)
    if len(match) != 1:
        return False, 'no matching int'
    hgt: int = int(match[0])

    if unit not in ['cm', 'in']:
        return False, 'invalid unit'

    if unit == 'in':
        if 59 <= hgt <= 76:
            return True, 'good'
        else:
            return False, f'{hgt}{unit} not valid'
    if unit == 'cm':
        if 150 <= hgt <= 193:
            return True, 'good'
        else:
            return False, f'{hgt}{unit} not valid'

    raise RuntimeError()

# %%


invalid_passports = ['eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926',
                     'iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946',
                     'hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277',
                     'hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007', ]

test_passports = ['pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f',
                  'eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm',
                  'hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022',
                  'iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719', ]

debug_file = open(au.get_debug_file_path('04'), 'w')


matching_data = []
spliting_pattern = re.compile('[\n\s:]+')

for pprt in valids:
    # for pprt in test_passports:
    pieces = spliting_pattern.split(pprt)
    assert (len(pieces) % 2 == 0)
    chunks = chunked(pieces, 2)
    d = {}
    for k, v in chunks:
        d[k] = v

    byr = int(d['byr'])
    if not (1920 <= byr <= 2002):
        debug_file.write(f'passing {d}, byr of {byr} invalid\n')
        continue

    iyr = int(d['iyr'])
    if not (2010 <= iyr <= 2020):
        debug_file.write(f'passing {d}, iyr of {iyr} invalid\n')
        continue

    eyr = int(d['eyr'])
    if not (2020 <= eyr <= 2030):
        debug_file.write(f'passing {d}, eyr of {eyr} invalid\n')
        continue

    hgt_str = d['hgt']
    hgt_is_valid, reason = height_valid(hgt_str)
    nl = "\n"
    if not hgt_is_valid:
        debug_file.write(f'passing {d} hgt {reason}{nl}')
        continue

    hcl = d['hcl']
    hcl_patt = re.compile('#[0-9a-f]{6}')
    if len(hcl_patt.findall(hcl)) != 1 or len(hcl) != 7:
        debug_file.write(f'passing {d}, hcl of {hcl} invalid\n')
        continue

    ecl = d['ecl']
    ecl_patt = re.compile('(amb|blu|brn|gry|grn|hzl|oth)')
    if len(ecl_patt.findall(ecl)) != 1 or len(ecl) != 3:
        debug_file.write(f'passing {d}, ecl of {ecl} invalid\n')
        continue

    pid = d['pid']
    pid_patt = re.compile('[0-9]{9}')
    if len(pid_patt.findall(pid)) != 1 or len(pid) != 9:
        debug_file.write(f'passing {d}, pid of {pid} invalid\n')
        continue

    matching_data.append(d)

debug_file.close()

print(len(matching_data))


with open('matches.txt', 'w') as f:
    f.write(pprint.pformat(matching_data))

# %
