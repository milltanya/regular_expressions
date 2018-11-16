import automaton
import unittest


class TestAutomaton(unittest.TestCase):
    def test_build_nfa(self):
        nfa = automaton.build_nfa('ab+')
        for i in range(len(nfa)):
            for j in range(len(nfa[i])):
                nfa[i][j] = (nfa[i][j].symbol, nfa[i][j].to)
        self.assertEqual(nfa, [[('a', 1), ('1', 2)], [('1', 3)], [('b', 3)], []])

    def test_delete_empty_edges(self):
        nfa = [[automaton.Edge('a', 1)],
               [automaton.Edge('1', 2)],
               [automaton.Edge('b', 3)],
               []]
        nfa = automaton.delete_empty_edges(nfa)
        self.assertEqual(nfa.first_vertex, 0)
        nfa = nfa.vertices
        for i in range(len(nfa)):
            for j in range(len(nfa[i])):
                nfa[i][j] = (nfa[i][j].symbol, nfa[i][j].to)
        self.assertEqual(nfa, [[automaton.Edge('a', 1)], [automaton.Edge('b', 3)], [], []])

    def test_build_dfa(self):
        nfa = automaton.NFA(
            0,
            [[automaton.Edge('a', 1),
              automaton.Edge('a', 2)],
             [automaton.Edge('b', 2)],
             [automaton.Edge('b', 3)],
             []]
        )
        self.assertEqual(automaton.build_dfa(nfa), [{'a': 1}, {'b': 2}, {'b': 3}, {}])

    def test_find_prefixes(self):
        self.assertEqual(automaton.find_prefixes('ab+c.aba.*.bac.+.+*', 'abacb'), 4)
        self.assertEqual(automaton.find_prefixes('acb..bab.c.*.ab.ba.+.+*a.', 'acbac'), 4)
        self.assertEqual(automaton.find_prefixes('acb..bab.c.*.ab.ba.+.+*a.', 'acbac'), 4)
        self.assertEqual(automaton.find_prefixes('aba.+*b.a.aab.+*.', 'ababba'), 4)
        self.assertEqual(automaton.find_prefixes('aba.+*b.a.aab.+*.', 'c'), 0)
        self.assertEqual(automaton.find_prefixes('1b+*', 'bbab'), 2)

    def test_find_prefixes_wrong_regular(self):
        with self.assertRaises(automaton.RPNError):
            automaton.find_prefixes('a+ba.+*b.a.aab.+*.', 'c')
    
    def test_build_automaton_empty_regular(self):
        self.assertEqual(automaton.build_automaton(''),
                         automaton.build_automaton('1'))

    def test_build_automaton(self):
        self.assertEqual(
            automaton.build_automaton('ab+*a.bc+a.*+'),
            [{'a': 0, 'b': 1, 'c': 2}, {'a': 0, 'b': 1, 'c': 2}, {'a': 0}])

    def test_build_automaton_wrong_regular(self):
        with self.assertRaises(automaton.RPNError):
            automaton.build_automaton('b+c.aba.*.bac.+.+*')
        with self.assertRaises(automaton.RPNError):
            automaton.build_automaton('ab+c.aba/.*.bac.+.+*')
        with self.assertRaises(automaton.RPNError):
            automaton.build_automaton('*ab+c.aba.*.bac.+.+*')


if __name__ == '__main__':
    unittest.main()
