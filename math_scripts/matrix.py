
def mat_mult(X, Y):
    assert len(X[0]) == len(Y)
    result = [[0] * len(Y[0])] * len(X)
    result = [[sum(a * b for a, b in zip(X_row, Y_col))
               for Y_col in zip(*Y)] for X_row in X]
    return result


def mat_print(mat):
    assert type(mat) == list and type(mat[0]) == list
    [print(repr(piece)) or '' + '\n' for piece in mat]



import math
from itertools import (combinations, combinations_with_replacement, count,
                       permutations)
from typing import List

import numpy as np
import scipy

help = "nMk: n choose k with multinomials\nnChoosek: n choosing k normally"


def nMk(n: int, k: [int]):
    """
    n choose k multinomially,
    """
    denom = 1
    for i in k:
        denom *= math.factorial(i)
    return math.factorial(n) / denom


def nChoosek(n: int, k: int):
    """
    normal n choose k
    """
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def partition(n: int, k: int):
    """
    partition of n identical elements into k unordered piles
    """
    if n == 0 and k == 0:
        return 1
    if k > n:
        return 0
    if k == 0 and n >= 1:
        return 0
    if k == 1:
        return 1
    if k == n:
        return 1
    return partition(n - 1, k - 1) + partition(n - k, k)


def pall(n):
    count = 0
    for k in range(0, n + 1):
        count += p(n, k)
    return count


def stirling(n: int, k: int):
    if k == 1 or n == k:
        return 1
    if k == 0:
        if n == 0:
            return 1
        return 0
    if k < 0 or k > n:
        return 0
    if n < 0 or k < 0:
        raise ValueError()
    first = k * stirling(n - 1, k)
    second = stirling(n - 1, k - 1)
    return first + second


def p_recursive(n):
    print(f"p{n} is ")
    for k in range(1, 15):
        print(f"k is {k}: {(-1) ** k} * (p{n - (k * (3 * k - 1) / 2)}) +p{n - (k * (3 * k + 1) / 2)})")


def snk(n, k):
    if k < 0:
        raise ValueError()
    if k == 1:
        return pall(n - 1)
    else:
        first = snk(n - 1, k - 1)
        second = snk(n - k, k - 1)
        return first - second


def lu_factor(A):
    """
        LU factorization with partial pivorting

        Overwrite A with:
            U (upper triangular) and (unit Lower triangular) L
        Return [LU,piv]
            Where piv is 1d numpy array with row swap indices
    """
    n = A.shape[0]
    piv = np.arange(0, n)
    for k in range(n - 1):

        # piv
        max_row_index = np.argmax(abs(A[k:n, k])) + k
        piv[[k, max_row_index]] = piv[[max_row_index, k]]
        A[[k, max_row_index]] = A[[max_row_index, k]]

        # LU
        for i in range(k + 1, n):
            A[i, k] = A[i, k] / A[k, k]
            for j in range(k + 1, n):
                A[i, j] -= A[i, k] * A[k, j]

    return [A, piv]


def matrix_cofactor(matrix):
    return np.linalg.inv(matrix).T * np.linalg.det(matrix)


def dist(t, u):
    dif_of_y = t[1] - u[1]
    dif_of_x = t[0] - u[0]
    return math.sqrt(dif_of_x**2 + dif_of_y**2)

def project(u,v):
    num = np.linalg.multi_dot([v,u])
    denom = np.linalg.multi_dot([u,u])
    print(f'num is {num}, denom is {denom}')
    div_result = num/denom
    print(f'div result is {div_result}')
    result = div_result *  u
    print(result)
    return result

def orth(a,b):
    return b - project(a,b)

def make_array_of_combinations(min,max, num) -> [int]:
    from itertools import combinations
    return combinations(range(min,max+1), num)

def find_span_vars(vectors:List[np.ndarray], vector:List[int]):
    gen = make_array_of_combinations(-15,15,len(vectors))
    matches = []
    from itertools import starmap
    import operator
    for candidate in gen:
        pairs = zip(vectors, candidate)
        after_multiplying = starmap(operator.mul, pairs)
        from functools import reduce
        added_vectors = reduce(operator.add, after_multiplying)
        if np.array_equal(added_vectors, vector):
            matches += [candidate]
    return matches


def row_echelon(A):
    """ Return Row Echelon Form of matrix A """

    # if matrix A has no columns or rows,
    # it is already in REF, so we return itself
    r, c = A.shape
    if r == 0 or c == 0:
        return A

    # we search for non-zero element in the first column
    for i in range(len(A)):
        if A[i,0] != 0:
            break
    else:
        # if all elements in the first column is zero,
        # we perform REF on matrix from second column
        B = row_echelon(A[:,1:])
        # and then add the first zero-column back
        return np.hstack([A[:,:1], B])

    # if non-zero element happens not in the first row,
    # we switch rows
    if i > 0:
        ith_row = A[i].copy()
        A[i] = A[0]
        A[0] = ith_row

    # we divide first row by first element in it
    A[0] = A[0] / A[0,0]
    # we subtract all subsequent rows with first row (it has 1 now as first element)
    # multiplied by the corresponding element in the first column
    A[1:] -= A[0] * A[1:,0:1]

    # we perform REF on matrix from second row, from second column
    B = row_echelon(A[1:,1:])

    # we add first row and first (zero) column, and return
    return np.vstack([A[:1], np.hstack([A[1:,:1], B]) ])

def is_orthogonal(vector_set:List):
    from itertools import permutations

    gen= permutations([np.array(item) for item in vector_set],2)

    def all_zeros(l):
        return all(item == 0 for item in l)

    if any(all_zeros(item) for item in vector_set):
        return False

    for vec1, vec2 in gen:
        dp = np.dot(vec1, vec2)
        if dp != 0:
            return False


vector_set = [
    [[1],[2],[-1],],
    [[1],[0],[1]],
    [[-1], [1], [1]]
]
data_xys = [
    (2,9),(3,10),(4,21),(5,20)
]

test_data = [
    (0,1),
    (1,2),
    (2,2),
    (3,4),
    (4,5),
]

def do_least_sqr_regress(pts:List[tuple])-> tuple:
    n= len(pts)
    x_s = [item[0] for item in pts]
    y_s = [item[1] for item in pts]

    sum_x = sum(x_s)
    sum_y = sum(y_s)

    sum_sqrd_x_s = sum(item[0]**2 for item in pts)

    sum_xy = 0

    for i, j in pts:
        sum_xy += i * j

    print(f'sum x is {sum_x}')
    print(f'sum y is {sum_y}')
    print(f'sum xy is {sum_xy}')
    print(f'sum_sqrd_x_s is {sum_sqrd_x_s}')

    m_num = (-1 * sum_x * sum_y + sum_xy * n)
    denom = (sum_sqrd_x_s * n) - (sum_x ** 2)
    m = m_num / denom

    b_num = (-1 * sum_x * sum_xy + sum_y * sum_sqrd_x_s)
    b = b_num / denom

    return m,b

v1 = np.array([3,0,-4])
v2 = np.array([11,0,2])
v3 = np.array([1,1,7])
minumum = -10
maximum = 40
gen =  permutations( range(minumum,maximum), 3)
counter = count(0)

x1 = np.array([[-1],[-4],[-3]])
x2 = np.array([[-1],[-2],[-2]])
x3 = np.array([[1],[1],[1]])

x4 = np.array([[3],[-4],[3]])

t1 = 2 * x1
t2 = 1 * x2
t3 = 0 * x3

to_factor = np.array([[2,3,3],[0,2,1],[4,6,1]])
def main():
    a = np.matrix([[-32, -6, 0], [194, 41, -21], [40, 8, -2]])
    x = np.matrix([[-6],[37],[8]])

    matches = []
    print(lu_factor(to_factor))
    import sys;sys.exit()

    for a1,a2,a3 in gen:
        val = next(counter)
        if val % 10000==0:
            print(f'{val/10000} ten thousands')


        p = np.array([
            [a1],[a2],[a3]])

        try:

            if np.array_equal(a @ p, 5*p):
                matches.append(p)
                print(p)
        except:
            continue
    return matches


def make_matrix_from_eigvect_eignval(p: np.matrix, d:np.matrix):
    """
    The Eigen- relationship can be represented by Ax=kx where A is the matrix, x is a vertical vector and k is some constant value.
    Example -
        p = np.matrix([ ## vector matrix where the verticla vectors are v1=[-1,-2,-2], v2=[-1,-4,-3], v3=[1,1,1]
            [-1, -1, 1],
            [-2, -4, 1],
            [-2, -3, 1]])
    d = np.matrix([ # Eigenvalues correspond as follows 1 <=> v1, 2 <=> v2, 0 <=> v3
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 0]])
    a = make_matrix_from_eigvect_eignval(p, d)
    :param p: Eigenvectors of the matrix. Each column represents a vertical vector x.
    :param d: Eigenvalues of the matrix. If it is an n*n matrix, then there should only be up to n non-zero entries.
    :return: Matrix that represents A where Ax = kx.
    """
    return p * d * np.linalg.inv(p)

def np_map(func, arr):

    return np.array([[func(xi) for xi in x] for x in arr])


if __name__ == "__main__":
    main()
    import sys; sys.exit()
    import numpy as np

    a = np.array([[-32, -6, 0], [194, 41, -21], [40, 8, -2]])
    from pprint import pprint
    from fractions import Fraction
    eigval,eigvect = np.linalg.eig(a)
    pprint(eigval)

    p = np.matrix([[-1, -1, 1], [-2, -4, 1], [-2, -3, 1]])
    d = np.matrix([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
    a = make_matrix_from_eigvect_eignval(p, d)


    if np.array_equal(a * x1, t1):
        if np.array_equal(a * x2, x2):
            print('two tests passed')
            print(a[1])

            if np.array_equal(a * x3, t3):
                print('three tests passed')
                print(a)


    print(a)

    print(a*x4)
