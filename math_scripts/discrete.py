import math

help = "nMk: n choose k with multinomials\nnChoosek: n choosing k normally"
def nMk(n:int, k:[int]):
	"""
	n choose k multinomially, 
	"""
	denom =1
	for i in k:
		denom *= math.factorial(i)
	return math.factorial(n)/denom

def nChoosek(n:int, k:int):
	"""
	normal n choose k
	"""
	return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))
def partition(n:int, k:int):
        """
        partition of n identical elements into k unordered piles
        """
        if n==0 and k==0:
                return 1
        if k> n:
                return 0
        if k == 0 and n >=1:
                return 0
        if k ==1:
                return 1
        if k == n:
                return 1
        return partition(n-1,k-1) + partition(n-k,k)
def pall(n):
        count =0
        for k in range(0,n+1):
                count += p(n,k)
        return count

def stirling(n:int, k:int):
        if k == 1 or n == k:
                return 1
        if k ==0:
                if n == 0:
                        return 1
                return 0
        if k< 0 or k >n:
                return 0
        if n<0 or k< 0:
                raise ValueError()
        first = k * stirling(n-1,k)
        second = stirling(n-1, k-1)
        return first + second
def p_recursive(n):
        print(f"p{n} is ")
        for k in range(1,15):
                print(f"k is {k}: {(-1)**k} * (p{n-(k*(3*k-1)/2)}) +p{n-(k*(3*k +1)/2)})")
def snk(n,k):
        if k<0:
                raise ValueError()
        if k==1:
                return pall(n-1)
        else:
                first = snk(n-1,k-1)
                second = snk(n-k,k-1)
                return first - second
        
nk = nChoosek
p = partition
print(p(10,3))
count =0
n = 10
for k in range(1,n+1):
        temp = stirling(n,k)
        print(f"stir({n},{k}) is {temp}")
        count += temp
print(count)
##print(count)
##print(f"p 52 is {pall(52)}")
##print(f"p 50 is {pall(50)}")
##p_recursive(52)



              
