from functools import reduce
import operator
num_ppl = 30
days_in_year = 365
iterable = (((days_in_year - i)/days_in_year) for i in range(num_ppl,0,-1))

prob_no_overlap = reduce(operator.mul,iterable )
print(prob_no_overlap)