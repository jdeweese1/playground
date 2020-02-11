'''
This is an example of a _very_ rudimentary interpreter. I decided to make this after taking a programming languages class, simply as a proof of concept
    Here is a sample program:
    [~] a 25;
    [<-] a [ 0 ] 1;
    print a ;
    [<-] a [ 23 ] 8;
    <- idx - 9 4 ;
    [<-] a [ idx ] 8;
    [<-] a [ 0 ] 2;
    if < 89 9 print 8 else print 7;
    print a ;
    <- a 9 ;
    <- b 4 ;
    print a ;
    while ( b ) { <- b 0 | } ;
    print b;


'''
from dataclasses import dataclass
from typing import List, Iterator, Iterable, Dict, Any
from itertools import count


@dataclass
class TokenHolder:
    def __init__(self):
        self.plus = '+'
        self.div = '/'
        self.modulus = '%'
        self.minus = '-'
        self.mult = '*'
        self.pow = '**'
        self.assignment = '<-'
        self.if_token = 'if'
        self.true_token = 'True'
        self.false_token = 'False'
        self.nl = '\n'
        self.semicolon = ';'
        self.print = 'print'
        self.input = 'input'
        self.while_token = 'while'
        self.l_paren = '('
        self.r_paren = ')'
        self.l_curly = '{'
        self.r_curly = '}'
        self.l_sq_bracket = '['
        self.r_sq_bracket = ']'
        self.arr_declare_token = '[~]'
        self.arr_index_assignment = '[<-]'
        self.arr_index_retrieve = '[->]'
        self.EOS_token = '|'
        self.lt_token = '<'
        self.eq_token = '=='
        self.def_token = 'def'

        self.op_tokens = [self.plus, self.div,
                          self.modulus, self.minus, self.mult, self.pow]
        self.arithmetic_compare_tokens = [self.lt_token, self.eq_token]
        self.keywords = [self.def_token, self.print, self.input,
                         self.while_token, self.true_token, self.false_token, self.if_token]


TH = TokenHolder()


class BinaryTree(object):
    __slots__ = ['value', 'left', 'right', ]

    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        if self.left is None and self.right is None:
            return f'Leaf({self.value})'
        return f'BT({self.left}, {self.value}, {self.right})'


class AssignmentValueTree(object):
    def __init__(self, var_name, exp):
        self.var_name = var_name
        self.exp = exp

    def __repr__(self):
        return f'Assignment({self.var_name} <- {self.exp})'


class ArrayDeclarationTree(object):
    def __init__(self, var_name: str, size: int):
        self.var_name = var_name
        self.size = size


@dataclass
class ArrayIndexAssignment(object):
    def __init__(self, arr_name: str, index_exp: BinaryTree, value_exp: BinaryTree):
        self.arr_name = arr_name
        self.index_exp = index_exp
        self.value_exp = value_exp


@dataclass
class ArrayIndexRetrieve(object):
    def __init__(self, arr_name: str, index_exp: BinaryTree):
        self.arr_name = arr_name
        self.index_exp = index_exp


class LeafPrint(object):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return f'LeafPrint(exp={self.exp})'


@dataclass
class LeafInput(object):
    pass


class WhileTree(object):
    def __init__(self, test_condition, if_true_exp):
        self.test_condition = test_condition
        self.if_true_exp = if_true_exp

    def __repr__(self):
        return f'WhileTree(test_condition={self.test_condition}, if_true_exp={self.if_true_exp}'


class VarLookup(object):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'VarLookup(token={self.token})'


@dataclass
class IfTree(object):
    def __init__(self, test_condition, if_true_exp, if_false_exp):
        self.test_condition = test_condition
        self.if_true_exp = if_true_exp
        self.if_false_exp = if_false_exp


@dataclass
class LTTree(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


@dataclass
class EqTree(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


@dataclass
class FuncDef(object):
    def __init__(self, name: str, kwargs: Dict[str, Any], executionTree):
        self.name = name
        self.kwargs = kwargs
        self.executionTree = executionTree


class Node(object):
    def __init__(self, value=None, next=None):
        super().__init__()
        self.value = value
        self.next = next

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value})'


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

    @staticmethod
    def from_iterable(it: Iterable):
        new = LinkedList()
        [new.append_val(item) for item in it]
        return new

    @property
    def head(self):
        return self.__head


class ArrayError(Exception):
    def __init__(self, *args):
        args = args
        super().__init__(ArrayError, *args)


class Arr(object):
    def __init__(self, size: int):
        self.size = size
        self.__l = [None] * size

    def set_at_index(self, index: int, value):
        if index > len(self.__l) + 1 or index < 0:
            raise ArrayError(
                f"Array of len {len(self.__l)} can't be indexed at {index}")
        else:
            self.__l[index] = value

    def get_at_index(self, index: int):
        if index > len(self.__l) + 1 or index < 0:
            raise ArrayError(
                f"Array of len {len(self.__l)} can't be indexed at {index}")
        else:
            return self.__l[index]

    @property
    def _l(self) -> list:
        return tuple(self.__l)

    def __str__(self):
        return str(self.__l)


def tokenize(line) -> list:
    tks = []
    for i, obj in enumerate(line.strip().split(' ')):
        tks.append(obj.strip())

    return tks


def parse_program(program: str) -> List[BinaryTree]:
    tree_list = []
    import re
    lines = re.split(';', program.strip())
    for line in lines:
        line = line.strip()
        if line == '' or line.startswith('#'):
            continue
        ll = LinkedList.from_iterable(it=tokenize(line))
        ll_iterator = iter(ll)
        tree_list.append(_parse(ll_iterator))
        [ll.append_val(item) for item in tokenize(line) if item != '']

    return tree_list


def _parse_to_token(ll_iterator: Iterator, token_to_stop_at: str) -> List:

    cur_tk = None
    exhausted_tks = []
    while cur_tk != token_to_stop_at:
        try:
            cur_tk = next(ll_iterator)
            exhausted_tks.append(cur_tk)
        except StopIteration:
            return exhausted_tks


def _parse(ll_iterator):
    tk = next(ll_iterator).value
    if not tk is None:

        if tk == TH.assignment:
            var_name = next(ll_iterator).value
            return AssignmentValueTree(var_name=var_name, exp=_parse(ll_iterator))
        elif tk.isnumeric():
            return BinaryTree(value=int(tk))

        elif tk == TH.if_token:
            test_cond = _parse(ll_iterator)

            if_true_exp = _parse(ll_iterator)
            assert next(ll_iterator).value == 'else'
            if_false_exp = _parse(ll_iterator)

            return IfTree(test_condition=test_cond, if_true_exp=if_true_exp, if_false_exp=if_false_exp)

        elif tk in TH.op_tokens:

            curr_tree = BinaryTree(left=_parse(
                ll_iterator), value=tk, right=_parse(ll_iterator))
            return curr_tree
        elif tk == TH.true_token:
            return BinaryTree(left=None, value=True, right=None)
        elif tk == TH.false_token:
            return BinaryTree(left=None, value=False, right=None)
        elif tk == TH.print:
            # TODO be able to handle printing an expression, not just a single value
            exp = next(ll_iterator)
            return LeafPrint(exp=exp.value)
        elif tk == TH.input:
            return LeafInput()
        elif tk == TH.nl:
            pass
        elif tk == TH.while_token:  # TODO fix to work with test condition that is expression
            # TODO fix to work with if_true_exp that is also multiline
            assert next(ll_iterator).value == TH.l_paren
            test_cond = _parse(ll_iterator)
            assert next(ll_iterator).value == TH.r_paren
            assert next(ll_iterator).value == TH.l_curly
            # This is v inefficient to cast iterator to list just to go back to iterator, and lots of padding, stripping and spliting that could be avoided
            body_of_while_str = ' '.join([item.value.strip() for item in _parse_to_token(
                ll_iterator, token_to_stop_at=TH.r_curly)]).split('|')
            body_tree_lines: list = []
            for line in body_of_while_str[:-1]:
                body_tree_lines.append(
                    _parse(iter(LinkedList.from_iterable(it=tokenize(line)))))
            # if_true_exp = _parse(ll_iterator)
            assert TH.r_curly in body_of_while_str[-1] and len(
                body_of_while_str[-1]) < 3
            return WhileTree(test_condition=test_cond, if_true_exp=body_tree_lines)
        elif tk.isalpha() and tk not in TH.keywords:
            return VarLookup(token=tk)
        elif tk == TH.arr_declare_token:
            var_name = next(ll_iterator).value
            assert var_name.isalpha()
            size = next(ll_iterator).value
            assert size.isnumeric()
            return ArrayDeclarationTree(var_name=var_name, size=size)
        elif tk == TH.arr_index_assignment:
            arr_var_name = next(ll_iterator).value
            assert arr_var_name.isalpha()
            assert next(ll_iterator).value == '['
            assignment_index_exp = _parse(ll_iterator)
            assert next(ll_iterator).value == ']'
            value = _parse(ll_iterator)
            return ArrayIndexAssignment(arr_name=arr_var_name, index_exp=assignment_index_exp, value_exp=value)
        elif tk == TH.arr_index_retrieve:
            arr_var_name = next(ll_iterator).value
            assert arr_var_name.isalpha()
            assert next(ll_iterator).value == '['
            assignment_index_exp = _parse(ll_iterator)
            assert next(ll_iterator).value == ']'

            return ArrayIndexRetrieve(arr_name=arr_var_name, index_exp=assignment_index_exp,)
        elif tk == TH.lt_token:
            lhs = _parse(ll_iterator)
            rhs = _parse(ll_iterator)
            return LTTree(lhs=lhs, rhs=rhs)

        elif tk == TH.eq_token:
            lhs = _parse(ll_iterator)
            rhs = _parse(ll_iterator)
            return EqTree(lhs=lhs, rhs=rhs)
        elif tk == TH.def_token:
            name = next(ll_iterator).value
            assert next(ll_iterator).value == '('
            assert next(ll_iterator).value == ')'
            assert next(ll_iterator).value == '{'
            return None
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


def _eval_tree_statement(t, env) -> EvaluationResult:
    if isinstance(t, BinaryTree) and t.left is None and t.right is None:
        return EvaluationResult(result=t.value, env=env)
    elif hasattr(t, 'value'):
        if t.value == TH.plus:
            sub_eval_result = _eval_tree_statement(t.left, env=env).result + _eval_tree_statement(t.right,
                                                                                                  env=env).result
            return EvaluationResult(result=sub_eval_result, env=env)
        elif t.value == TH.div:
            sub_eval_result = _eval_tree_statement(t.left, env=env).result // _eval_tree_statement(t.right,
                                                                                                   env=env).result
            return EvaluationResult(result=sub_eval_result, env=env)
        elif t.value == TH.modulus:
            sub_eval_result = _eval_tree_statement(t.left, env=env).result % _eval_tree_statement(t.right,
                                                                                                  env=env).result
            return EvaluationResult(result=sub_eval_result, env=env)
        elif t.value == TH.minus:
            sub_eval_result = _eval_tree_statement(t.left, env=env).result - _eval_tree_statement(t.right,
                                                                                                  env=env).result
            return EvaluationResult(result=sub_eval_result, env=env)
        elif t.value == TH.mult:
            sub_eval_result = _eval_tree_statement(t.left, env=env).result * _eval_tree_statement(t.right,
                                                                                                  env=env).result
            return EvaluationResult(result=sub_eval_result, env=env)
        elif t.value == TH.pow:
            sub_eval_result = _eval_tree_statement(t.left, env=env).result ** _eval_tree_statement(t.right,
                                                                                                   env=env).result
            return EvaluationResult(result=sub_eval_result, env=env)
    elif isinstance(t, AssignmentValueTree):
        eval_result = _eval_tree_statement(t.exp, env=env)
        env[t.var_name] = eval_result.result
        return EvaluationResult(result=True, env=env)
    elif t == TH.true_token:
        return EvaluationResult(result=True, env=env)
    elif isinstance(t, LeafPrint):
        if t.exp in env:
            print(env[t.exp])
        else:
            print(t.exp)
        return EvaluationResult(result=True, env=env)
    elif isinstance(t, LeafInput):
        text_input = input('>>> ')
        return EvaluationResult(result=text_input, env=env)
    elif isinstance(t, IfTree):
        truth_condition_holds = bool(
            _eval_tree_statement(t.test_condition, env=env).result)

        if truth_condition_holds:  # fixme to not be string
            r = _eval_tree_statement(t=t.if_true_exp, env=env).result
        else:
            r = _eval_tree_statement(t=t.if_false_exp, env=env).result
        return EvaluationResult(result=r, env=env)
    elif isinstance(t, VarLookup):
        var_is_defined = t.token in env
        if var_is_defined:
            return EvaluationResult(result=env.get(t.token), env=env)
        else:
            raise EvalError(
                f'Var or func {{{t.token}}} is not defined in current scope')
    elif isinstance(t, WhileTree):
        test_cond = t.test_condition
        if_true_exp = t.if_true_exp
        max_while_depth_per_loop = 1024
        counter = count(1)

        while bool(_eval_tree_statement(test_cond, env=env).result):
            if next(counter) >= max_while_depth_per_loop:
                raise EvalError(
                    f'Max while depth of {max_while_depth_per_loop} exceeded ')
            result = _eval_tree_lines(if_true_exp, env=env)

        return result
    elif isinstance(t, ArrayDeclarationTree):
        name = t.var_name
        size = t.size
        assert size.isnumeric()
        env[name] = Arr(size=int(size))
        return EvaluationResult(result=True, env=env)
    elif isinstance(t, ArrayIndexAssignment):
        if t.arr_name not in env:
            raise EvalError(
                f'Var or func {{{t.arr_name}}} is not defined in current scope')
        else:
            arr: Arr = env.get(t.arr_name)
            index = _eval_tree_statement(t.index_exp, env=env).result
            value = _eval_tree_statement(t.value_exp, env=env).result
            arr.set_at_index(index=index, value=value)
            return EvaluationResult(True, env)
    elif isinstance(t, ArrayIndexRetrieve):
        if t.arr_name not in env:
            raise EvalError(
                f'Var or func {{{t.arr_name}}} is not defined in current scope')
        else:
            arr: Arr = env.get(t.arr_name)
            index = _eval_tree_statement(t.index_exp, env=env).result
            result = arr.get_at_index(index=index)
            return EvaluationResult(result, env)
    elif isinstance(t, EqTree):
        lhs_result = _eval_tree_statement(t=t.lhs, env=env).result
        rhs_result = _eval_tree_statement(t=t.rhs, env=env).result
        cond_passes = lhs_result == rhs_result

        return EvaluationResult(result=cond_passes, env=env)
    elif isinstance(t, LTTree):
        lhs_result = _eval_tree_statement(t=t.lhs, env=env).result
        rhs_result = _eval_tree_statement(t=t.rhs, env=env).result
        cond_passes = lhs_result < rhs_result

        return EvaluationResult(result=cond_passes, env=env)

    else:
        raise EvalError(
            f'No definition for how to eval a {t.__class__.__name__} "{t}"')


def eval_tree_lines(lines):
    return _eval_tree_lines(lines, env={})


def _eval_tree_lines(lines: List[BinaryTree], env) -> EvaluationResult:
    result = EvaluationResult(result=None, env=env)
    for tree in lines:
        result = _eval_tree_statement(tree, result.env)
    return result


def run_program(program: str):
    program_tree_lines = parse_program(program)
    r = eval_tree_lines(program_tree_lines)
    return r


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    file_p = args.file
    with open(file_p, 'r') as file_reader:
        program = file_reader.read()
        print(program)
    sep = '-' * 15
    print(sep)
    program_result = run_program(program).result
    print(sep)
    print(program_result)
