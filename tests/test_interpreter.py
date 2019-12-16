from unittest import TestCase
from unittest.case import TestCase

from interpreter import run_program
from interpreter import LinkedList


class TestArithmetic(TestCase):
    def test_arithmetic(self):
        self.assertEqual(run_program('4').result, 4)
        self.assertEqual(run_program('* 9 6 ').result, 54)
        self.assertEqual(run_program('/ * 9 6 2').result, 27)
        self.assertEqual(run_program('* / 21 3 5').result, 35)


class TestVariableBinding(TestCase):
    def test_env(self):
        self.assertDictEqual(run_program('<- a * / 21 3 5').env, {'a': 35})


class TestRunProgram(TestCase):

    def test_if_else(self):
        self.assertEqual(run_program('if True True else False').result, True)
        self.assertEqual(run_program('if 0 True else False').result, False)
        self.assertEqual(run_program('if True 5 else 4').result, 5)
        self.assertEqual(run_program('if True + 4 5 else * 4 9').result, 9)
        self.assertEqual(run_program('if 1 + 4 5 else * 4 9').result, 9)
        self.assertEqual(run_program('if False + 4 5 else * 4 9').result, 36)
        self.assertEqual(run_program('if 0 + 4 5 else * 4 9').result, 36)
        self.assertEqual(run_program('if - 5 5 + 4 5 else * 4 9').result, 36)
        self.assertDictEqual(run_program('<- a if - 5 5 + 4 5 else * 4 9').env, {'a': 36})

    def test_with_nl_in_program(self):
        self.assertEqual(run_program('<- a - 9 8 ; + a 1').result, 2)


class TestLinkedList(TestCase):
    def test_iter(self):
        l = [i for i in range(0,10)]
        ll = LinkedList()
        [ll.append_val(item) for item in l]

        ll_iterator = iter(ll)

        ll_items = [ll_item.value for ll_item in ll_iterator]
        self.assertListEqual(ll_items, l)

