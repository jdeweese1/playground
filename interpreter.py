from dataclasses import dataclass


@dataclass
class TokenHolder:
    def __init__(self):
        self.plus = '+'
        self.div = '/'
        self.modulus = '%'
        self.minus = '-'
        self.mult = '*'
        self.assignment = '<-'
        self.if_token = 'if'
        self.true_token = 'True'
        self.false_token = 'False'
        self.nl = '\n'
        self.semicolon = ';'

        self.op_tokens = [self.plus, self.div, self.modulus, self.minus, self.mult]


TH = TokenHolder()


class BinaryTree(object):
    __slots__ = ['value', 'left', 'right', ]

    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        if self.left == None and self.right == None:
            return f'Leaf({self.value})'
        return f'BT({self.left}, {self.value}, {self.right})'


class AssignmentTree(object):
    def __init__(self, var_name, exp):
        self.var_name = var_name
        self.exp = exp

    def __repr__(self):
        return f'Assignment({self.var_name} <- {self.exp})'


@dataclass
class IfTree(object):
    def __init__(self, test_condition, if_true_exp, if_false_exp):
        self.test_condition = test_condition
        self.if_true_exp = if_true_exp
        self.if_false_exp = if_false_exp


class Stack(object):
    def __init__(self):
        super().__init__()
        self.__l = []

    def push(self, value):
        self.__l.append(value)

    def pop(self):
        if len(self.__l) > 0:
            return self.__l.pop()

    def peek(self):
        if len(self.__l) > 0:
            return self.__l[-1]


class Node(object):
    def __init__(self, value=None, next=None):
        super().__init__()
        self.value = value
        self.next = next

    def __repr__(self):
        return f'{self.__class__.__name__}(val={self.value})'


class LinkedList(object):
    def __init__(self):
        self.__head = None
        self.__tail = None

    def append_val(self, value):
        new_node = Node(value)
        if self.__head is None:
            self.__head = new_node
            self.__head.next = None
            self.__tail = new_node
        else:
            self.__tail.next = new_node
            self.__tail = new_node

    def __iter__(self):
        cur = self.__head

        while cur != None:
            yield cur
            cur = cur.next

    @property
    def head(self):
        return self.__head


def parse_program(program: str) -> BinaryTree:
    ll = LinkedList()
    import re

    [ll.append_val(item) for item in re.split(' ', program.strip())]
    ll_iterator = iter(ll)

    return _parse(ll_iterator)


def _parse(ll_iterator):
    tk = next(ll_iterator).value

    if not tk is None:

        if tk == TH.assignment:
            var_name = next(ll_iterator).value
            return AssignmentTree(var_name=var_name, exp=_parse(ll_iterator))
        elif tk.isnumeric():
            return BinaryTree(value=int(tk))

        elif tk == TH.if_token:
            test_cond = _parse(ll_iterator)

            if_true_exp = _parse(ll_iterator)
            assert next(ll_iterator).value == 'else'
            if_false_exp = _parse(ll_iterator)

            return IfTree(test_condition=test_cond, if_true_exp=if_true_exp, if_false_exp=if_false_exp)

        elif tk in TH.op_tokens:

            curr_tree = BinaryTree(left=_parse(ll_iterator), value=tk, right=_parse(ll_iterator))
            return curr_tree
        elif tk == TH.true_token:
            return BinaryTree(left=None, value=True, right=None)
        elif tk == TH.false_token:
            return BinaryTree(left=None, value=False, right=None)
        elif tk == TH.nl:
            pass
        else:
            raise ParseError(f'uh oh received {tk}')

    else:
        raise ParseError(f"token was bad {tk}")


class ParseError(BaseException):

    def __init__(self, *args):
        args = args
        super().__init__(ParseError, *args)


class EvalError(BaseException):

    def __init__(self, *args):
        args = args
        super().__init__(EvalError, *args)


@dataclass
class EvaluationResult(object):
    __slots__ = ['result', 'env']

    def __init__(self, result, env: dict):
        self.result = result
        self.env = env

    def __repr__(self):
        return f'EvaluationResult(result={self.result})'


def _eval_tree(t, env) -> EvaluationResult:
    if isinstance(t, BinaryTree) and t.left == None and t.right == None:
        return EvaluationResult(result=t.value, env=env)
    elif hasattr(t, 'value'):
        if t.value == TH.plus:
            sub_eval_result = _eval_tree(t.left, env=env).result + _eval_tree(t.right, env=env).result
            return EvaluationResult(result=sub_eval_result, env=env)
        elif t.value == TH.div:
            sub_eval_result = _eval_tree(t.left, env=env).result // _eval_tree(t.right, env=env).result
            return EvaluationResult(result=sub_eval_result, env=env)
        elif t.value == TH.modulus:
            sub_eval_result = _eval_tree(t.left, env=env).result % _eval_tree(t.right, env=env).result
            return EvaluationResult(result=sub_eval_result, env=env)
        elif t.value == TH.minus:
            sub_eval_result = _eval_tree(t.left, env=env).result - _eval_tree(t.right, env=env).result
            return EvaluationResult(result=sub_eval_result, env=env)
        elif t.value == TH.mult:
            sub_eval_result = _eval_tree(t.left, env=env).result * _eval_tree(t.right, env=env).result
            return EvaluationResult(result=sub_eval_result, env=env)
    elif isinstance(t, AssignmentTree):
        env[t.var_name] = _eval_tree(t.exp, env=env).result
        return EvaluationResult(result=True, env=env)
    elif t == TH.true_token:
        return EvaluationResult(result=True, env=env)
    elif isinstance(t, IfTree):
        truth_condition_holds = bool(_eval_tree(t.test_condition, env=env).result)

        if truth_condition_holds:  # fixme to not be string
            r = _eval_tree(t=t.if_true_exp, env=env).result
        else:
            r = _eval_tree(t=t.if_false_exp, env=env).result
        return EvaluationResult(result=r, env=env)
    else:
        raise EvalError(f'No definition for how to eval a {t.__class__.__name__} "{t}"')


def eval_tree(t):
    env = {}
    return _eval_tree(t, env)


def run_program(program: str):
    tree = parse_program(program)
    r = eval_tree(tree)
    return r


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    file_p = args.file
    with open(file_p, 'r') as file_reader:
        program = file_reader.readline()
        print(program)
    print(run_program(program).result)
