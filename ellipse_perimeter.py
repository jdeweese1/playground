from matplotlib import pyplot as plt
import numpy as np
import math
from cachier import cachier
import typing

Point = typing.Tuple[float, float]


def dist_points(pt1: Point, pt2:Point):
    x1, y1 = pt1
    x2, y2 = pt2

    return math.sqrt((y2-y1)**2 + (x1-x2)**2)


@cachier()
def brute_force_perimeter(a,b):
    range_start = 0
    range_end = a
    args = [range_start, range_end, .000001]
    x = np.arange(*args)

    @cachier()
    def graph_peri_func(x, a, b):
        x2_over_a2 = x ** 2 / a ** 2
        inner = 1 - x2_over_a2
        ret_val = b * math.sqrt(inner)
        return ret_val

    y = [graph_peri_func(x=x_val, a=a, b=b) for x_val in x]
    points = zip(x, y)

    last_point = (0, b)
    total_dist_of_arc = 0
    el_points_iter = iter(points)
    for point in el_points_iter:
        tmp_dist = dist_points(last_point, point)
        total_dist_of_arc += tmp_dist
        last_point = point
    return total_dist_of_arc * 4


def two_pi_sqrt_mult_a_b(a,b):
    return 2 * math.pi * math.sqrt(a * b)


def ram_best(a,b):
    h = get_h(a, b)
    return math.pi* (a + b) * (1 + (3 * h)/(10 + math.sqrt(4-3*h)))


def get_h(a, b):
    num = (a - b) ** 2
    denom = (a + b) ** 2
    h = num / denom
    return h


def parker_best(a,b):
    return math.pi * ((53*a/3) + (717*b/35) - math.sqrt(269* a**2 + 667*a*b + 371*b**2))


def jarod_best(a,b):
    if b/a <= 15:
        return parker_best(a,b)
    return 1.25 * math.pi * b * a


def calculate_perimeter_ram_other(a, b):
    perimeter = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))
    return perimeter


def bin_coef(n,r):
    return math.gamma(n +1) /\
           (math.gamma(r+1) *
            math.gamma(n - r + 1))


def peri_infinite_sum(a,b) -> float:
    coef = math.pi * (a + b)
    h = get_h(a,b)

    c = range(0,11)
    gen = (bin_coef(.5, n)**2 * h**n for n in c)
    return coef * sum(gen)

def linear_perimeter(a,b):
    ratio = b/a
    return 3.915 * ratio + 1.715



def main():
    start_ratio = 1
    ratio_to_approach = 20
    POINTS_SOURCE_MAP = [
        # ('brute force distance', brute_force_perimeter),
        ('ram_best', ram_best),
        ('parker_best', parker_best),
        ('jarod_best', jarod_best),
        ('ram_other', calculate_perimeter_ram_other),
        ('', peri_infinite_sum),
    ]
    res_map = {}
    x_vals = np.arange(start_ratio, ratio_to_approach, .2)
    a = 1

    for label, func in POINTS_SOURCE_MAP:
        func_error_vals = []
        for i in x_vals:
            b = a * i
            true_perimeter = peri_infinite_sum(a, b)
            if func == peri_infinite_sum:
                res = true_perimeter
            else:
                res = func(a, b)
            pct_error = 100 * abs(res - true_perimeter) / true_perimeter
            func_error_vals.append({
                'pct_error': pct_error,
                'true_val': true_perimeter,
                'guess': res,
            })

        res_map[func.__name__] = func_error_vals
    for func_name, func_metrics_list in res_map.items():
        plt.plot(x_vals, [item['pct_error'] for item in func_metrics_list], label=func_name)
    plt.legend()
    plt.show()
    return res_map


if __name__ == '__main__':
    # main()
    x = np.arange(0,1,.2)
    y_correct = list(map(lambda item: peri_infinite_sum(1, item), x))
    y_ram = np.fromiter(map(lambda item: ram_best(1, item), x), dtype=np.float)
    y_jarod = np.fromiter(map(lambda item: jarod_best(1, item), x), dtype=np.float)
    y_lin = np.fromiter(map(lambda item: linear_perimeter(1, item), x), dtype=np.float)

    r = np.polynomial.polynomial.Polynomial.fit(x=x, y=y_correct, deg=1,)
    plt.plot(x, y_correct, label='correct')
    # plt.plot(x, y_ram, label='ram')
    # plt.plot(x, y_jarod, label='jarod')
    # plt.plot(x, y_lin, label='lin')
    plt.legend()
    plt.show()
