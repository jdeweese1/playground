import json
import os
from pathlib import Path

debug_dir = Path('logging')
if not debug_dir.exists():
    os.mkdir(debug_dir.absolute())
NL = '\n'
ES = ''


def get_debug_file_path(day=None):
    fn = f'debug{day or ES }.txt'
    return debug_dir.joinpath(fn)


def write_to_debug_file_path(s: str, day = None):
    with open(get_debug_file_path(day), 'w') as f_writes:
        f_writes.write(s)


def _get_input_fn(s):
    return f'dec_{s}_input.json'


def obtain_input_for_day(s:str):
    with open(_get_input_fn(s), 'r') as f_reads:
        return json.loads(f_reads.read())
