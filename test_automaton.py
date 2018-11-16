import automaton
import unittest


class TestAutomaton(unittest.TestCase):

    def test_find_prefixes_1(self):
        self.assertEqual(automaton.find_prefixes('ab+c.aba.*.bac.+.+*',
                                                 'abacb'), 4)

    def test_find_prefixes_2(self):
        self.assertEqual(automaton.find_prefixes('acb..bab.c.*.ab.ba.+.+*a.',
                                                 'acbac'), 4)

    def test_find_prefixes_3(self):
        self.assertEqual(automaton.find_prefixes('aba.+*b.a.aab.+*.',
                                                 'ababba'), 4)

    def test_find_prefixes_4(self):
        self.assertEqual(automaton.find_prefixes('aba.+*b.a.aab.+*.', 'c'), 0)

    def test_find_prefixes_5(self):
        self.assertEqual(automaton.find_prefixes('1b+*', 'bbab'), 2)

    def test_find_prefixes_wrong_regular(self):
        with self.assertRaises(automaton.RPNError):
            automaton.find_prefixes('a+ba.+*b.a.aab.+*.', 'c')

    def test_build_automaton_empty_regular(self):
        self.assertEqual(automaton.build_automaton(''),
                         automaton.build_automaton('1'))

    def test_build_automaton_1(self):
        self.assertEqual(
            automaton.build_automaton('ab+*a.bc+a.*+'),
            [{'a': 0, 'b': 1, 'c': 2}, {'a': 0, 'b': 1, 'c': 2}, {'a': 0}])

    def test_build_automaton_wrong_regular_1(self):
        with self.assertRaises(automaton.RPNError):
            automaton.build_automaton('b+c.aba.*.bac.+.+*')

    def test_build_automaton_wrong_regular_2(self):
        with self.assertRaises(automaton.RPNError):
            automaton.build_automaton('ab+c.aba/.*.bac.+.+*')

    def test_build_automaton_wrong_regular_3(self):
        with self.assertRaises(automaton.RPNError):
            automaton.build_automaton('*ab+c.aba.*.bac.+.+*')


if __name__ == '__main__':
    unittest.main()
