from unittest.case import TestCase
from unittest import mock
from interpreter import run_program
from interpreter import LinkedList


class TestArithmetic(TestCase):
    def test_arithmetic(self):
        self.assertEqual(run_program(' 4 ').result, 4)
        self.assertEqual(run_program('* 9 6').result, 54)
        self.assertEqual(run_program('/ * 9 6 2').result, 27)
        self.assertEqual(run_program('* / 21 3 5').result, 35)
        self.assertEqual(run_program('** 2 3').result, 8)


class TestVariableBinding(TestCase):
    def test_env(self):
        self.assertDictEqual(run_program('<- a * / 21 3 5').env, {'a': 35})

    def test_array_decl(self):
        program = """
        [~] a 10;
        """

        result = run_program(program=program)

        self.assertTupleEqual(result.env['a']._l, tuple([None]*10))

    def test_array_set(self):
        program = """
        [~] arr 10;
        [<-] arr [ 0 ]  9;
        [<-] arr [ 9 ]  7;"""

        result = run_program(program=program)
        self.assertTupleEqual(result.env['arr']._l, (9, *[None] * 8, 7))

    def test_array_get(self):
        program = '''
        [~] arr 4;
        [<-] arr [ 2 ] 7 ;
        <- a [->] arr [ 2 ] ;
'''
        result = run_program(program=program)
        self.assertEqual(result.env['a'], 7)


class TestLeafInput(TestCase):
    def setUp(self) -> None:
        super().setUp()

    @mock.patch('builtins.input', lambda *arg: '89')
    def test_input(self):
        program = '''
        <- e input;'''
        result = run_program(program)
        self.assertEqual(result.env['e'], '89')


class TestWhile(TestCase):
    pass


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
        self.assertDictEqual(run_program(
            '<- a if - 5 5 + 4 5 else * 4 9').env, {'a': 36})

    def test_with_nl_in_program(self):
        self.assertEqual(run_program('<- a - 9 8 ;\n<- a + a 1').env, {'a': 2})


class TestLinkedList(TestCase):
    def test_iter(self):
        l = [i for i in range(0, 10)]
        ll = LinkedList()
        [ll.append_val(item) for item in l]

        ll_iterator = iter(ll)

        ll_items = [ll_item.value for ll_item in ll_iterator]
        self.assertListEqual(ll_items, l)
