from collections import Counter
from typing import List


def is_stepping(n: int) -> bool:
    if n <= 10:
        return True

    def diff_is_one(a, b):
        return abs(a-b) == 1
    last_digit = n % 10
    candidate_num = n // 10
    return diff_is_one(last_digit, candidate_num % 10) and is_stepping(candidate_num)


def is_colorful():
    '''
    Means all substrings products are distinct
    :return:
    '''
    pass


def replace_min_max(in_str: str):
    c = Counter(in_str.replace(' ', ''))
    commons = c.most_common()
    most_common_tup, *_, least_common_tup = commons
    max_num = most_common_tup[1]
    min_num = least_common_tup[1]
    def to_ascii(x): return ord(x[0])
    min_ord = ord(
        min([item for item in commons if item[1] == min_num], key=to_ascii)[0])
    max_ord = ord(
        min([item for item in commons if item[1] == max_num], key=to_ascii)[0])
    d = {min_ord: max_ord, max_ord: min_ord}
    return in_str.translate(d)


def find_longest_snake():
    pass


def _partition(s) -> List[str]:
    if len(s) <= 1:
        return [s]
    else:
        for i in range(1, len(s)):
            l = [s[:i]]
            r = s[i:]
            # matches.append([*l, *r])
            result = _partition(r)
            yield from (l + item for item in result)
            print(f'{result}')


s = 'The quick brown fox jumped over the lazy doggo.'
print(replace_min_max(s))

if __name__ == '__main__':
    # result = list(_partition('1234'))
    # print(result)
