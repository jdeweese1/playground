import itertools as itrls

import more_itertools as mi

from aoc import aoc_utils as au

inp = au.obtain_input_for_day('07')
debug_path = au.get_debug_file_path('07')


def parse_second_half(s):
    contained_inside = s.split(',')
    cleaned_bags = [bag.strip().replace('bags', 'bag')
                    for bag in contained_inside]
    return cleaned_bags


def parse_inp():
    r = []
    for line in inp:
        d = {}
        bag, can_contain_s = line.split('contain')
        d['bag'] = bag.replace('bags', 'bag').strip()
        d['can_contain_s'] = can_contain_s
        can_contain = parse_second_half(can_contain_s)
        d['can_contain'] = can_contain

        r.append(d)
    return r


# %%
bag_rules = parse_inp()
search_for = set()
search_for.add('shiny gold bag')
for i in range(100):
    for d in bag_rules:
        bag, bags_that_could_be_contained = d['bag'], d['can_contain_s']
        if any(candidate in bags_that_could_be_contained for candidate in search_for):
            search_for.add(bag)
    print(len(search_for))


# %%


# %%


class Bag:
    objects = set()

    @staticmethod
    def reset():
        Bag.objects = set()

    def __init__(self, name):
        name = name.strip()
        self.contains = set()
        Bag.objects.add(self)

        self.name = name

    def add_contains(self, quan, name):
        if 'no other bag' not in name:
            self.contains.add((quan, name))

    def get_contained_bags_and_counts(self):
        return [(t[0], self.obtain_bag_for_name(t[1])) for t in self.contains]

    @staticmethod
    def obtain_bag_for_name(name):
        for o in Bag.objects:
            if o.name == name:
                return o

    def __repr__(self):
        return f'Bag(name={self.name},contains={self.contains}'


# %%
Bag.reset()
bag_rules = parse_inp()
search_for = set()
search_for.add('shiny gold bag')
for d in bag_rules:
    bag = d['bag']
    contaning_bag = Bag(name=bag)
    bags_that_could_be_contained: list = []

    for cable in d['can_contain']:
        if cable == 'no other bag':
            continue
        quan = int(cable[0])
        contaning_bag.add_contains(quan, cable[1:].strip())

# %%
bag_count = 0
stack = [(1, Bag.obtain_bag_for_name('shiny gold bag'))]
history = []
while len(stack) > 0:
    mult_power, b = stack.pop()
    print(b)
    for quan, contained_bag in b.get_contained_bags_and_counts():
        bag_count += quan * mult_power
        contained_bag_s = contained_bag.name
        print(contained_bag_s)
        new_bag_to_dive = Bag.obtain_bag_for_name(contained_bag_s)
        assert new_bag_to_dive != None
        stack.append((quan * mult_power, new_bag_to_dive))
print(bag_count)
