from typing import Callable
import math
import itertools

def create_geo_pmf(p:int) -> Callable:
    f = lambda x: ((1 -p)**(x-1)) *p
    return f

def nChooseK(n:int, k:int):
	if n < 0 or k < 0 or k > n:
		raise ValueError(f'n was {n} k was {k}')
	top = math.factorial(n)
	bottom = (math.factorial(n-k) * math.factorial(k))
	return int(top/bottom)

def create_bin_bernoulli_pmf(p) -> Callable:
	def temp_func(x:int, n:int) -> int:
		first = nChooseK(n,x)
		second = p ** x
		third = (1-p)**(n-x)
		return first * second * third
	return temp_func

def create_neg_bin_dist(p:float) -> Callable:
	if p < 0 or p > 1:
		raise ValueError(f'p was {p}')
	def temp_func(x,r):
		"""
			x is number of bernoulli trials to have r successes
		"""
		first = nChooseK(x-1, r-1)
		second = (1-p) ** (x-r)
		third = p ** r
		# print(f'{first} {second} {third}')
		return first * second * third
	return temp_func

def poisson(lambd:float, x:float):
	top = (lambd ** x)* (math.e ** (-1 * lambd))
	bottom = math.factorial(x)
	return top/bottom

