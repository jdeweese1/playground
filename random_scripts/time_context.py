import time
from contextlib import contextmanager
@contextmanager
def time_context():
    enter_time = time.time()
    yield
    end_time = time.time()
    elapsed = end_time - enter_time
    print(f'Took {elapsed}')



with time_context() as t:
    input()
