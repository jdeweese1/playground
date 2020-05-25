import os
import sys
import argparse
from itertools import count
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument("search_path", type=Path)
parser.add_argument("pattern", type=str)
parser.add_argument("--exclude", metavar='N', nargs='+', type=str, default='__')

args = parser.parse_args()
root_search_dir = args.search_path
pattern = args.pattern
exclude = args.exclude
matches = []
for cur_dir, dirs, filenames in os.walk(root_search_dir):
    [matches.append(os.path.join(cur_dir, filename)) for filename in filter(lambda f: pattern in f and all([exclude_pattern not in f for exclude_pattern in exclude]), filenames)]
    [matches.append((os.path.join(cur_dir, dir_name))) for dir_name in filter(lambda d: pattern in d and all([exclude_pattern not in d and exclude_pattern not in cur_dir for exclude_pattern in exclude]), dirs)]

counter = count()
[print(f'{next(counter)}: {match}') for match in matches]

