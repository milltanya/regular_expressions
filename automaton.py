from collections import namedtuple


class RPNError(Exception):
    def __init__(self, regular_expression, message):
        self.regular_expression = regular_expression
        self.message = message

    def __str__(self):
        return f"Error in the Reverse Polish notation " \
               f"'{self.regular_expression}': {self.message}"


Edge = namedtuple('Edge', ['symbol', 'to'])
Pair = namedtuple('Pair', ['start', 'end'])
NFA = namedtuple('Automaton', ['first_vertex', 'vertices'])


def build_nfa(reg):
    """
    build NFA
    """
    stack = []
    vertices = []
    for symbol in reg:
        if symbol.isalpha() or symbol == '1':
            start = len(vertices)
            end = start + 1
            vertices.append([Edge(symbol, end)])
            vertices.append([])
            stack.append(Pair(start, end))
        else:
            if symbol == '.':
                if len(stack) < 2:
                    raise RPNError(reg, ". is a binary operation")
                second = stack.pop()
                first = stack.pop()
                vertices[first.end].append(Edge('1', second.start))
                stack.append(Pair(first.start, second.end))
            else:
                if symbol == '+':
                    if len(stack) < 2:
                        raise RPNError(reg, "+ is a binary operation")
                    second = stack.pop()
                    first = stack.pop()
                    vertices[first.start].append(Edge('1', second.start))
                    vertices[first.end].append(Edge('1', second.end))
                    stack.append(Pair(first.start, second.end))
                else:
                    if symbol == '*':
                        if len(stack) < 1:
                            raise RPNError(reg, "* is an unary operation")
                        last = stack.pop()
                        vertices[last.end].append(Edge('1', last.start))
                        stack.append(Pair(last.start, last.start))
                    else:
                        raise RPNError(reg, "unknown symbol")
    if len(stack) != 1:
        raise RPNError(reg, "more than 1 element in the stack at the "
                            "end of the expression")
    return vertices


def delete_empty_edges(vertices):
    """
    delete empty edges
    """
    first_vertex = 0
    for start in range(len(vertices)):
        i = 0
        while i < len(vertices[start]):
            edge = vertices[start][i]
            if edge.symbol == '1':
                vertices[start].remove(edge)
                end = edge.to
                if start != end:
                    if first_vertex == end:
                        first_vertex = start
                    vertices[start].extend(vertices[end])
                    vertices[end].clear()
                    for a in range(len(vertices)):
                        j = 0
                        while j < len(vertices[a]):
                            a_edge = vertices[a][j]
                            if a_edge.to == end:
                                vertices[a].remove(a_edge)
                                vertices[a].append(Edge(a_edge.symbol, start))
                            else:
                                j += 1
            else:
                i += 1
    return NFA(first_vertex, vertices)


def build_dfa(nfa):
    """
    build DFA
    """
    first_vertex = nfa.first_vertex
    vertices = nfa.vertices
    classes = [[first_vertex]]
    automaton = []
    i = 0
    while i < len(classes):
        edges = {}
        for vertex in classes[i]:
            for edge in vertices[vertex]:
                if edge.symbol not in edges.keys():
                    edges[edge.symbol] = []
                if edge.to not in edges[edge.symbol]:
                    edges[edge.symbol].append(edge.to)
        automaton.append({})
        for symbol in edges.keys():
            edges[symbol].sort()
            if edges[symbol] not in classes:
                classes.append(edges[symbol])
            number = classes.index(edges[symbol])
            automaton[i][symbol] = number
        i += 1
    return automaton


def build_automaton(reg):
    if reg is '':
        return [{}]
    nfa = build_nfa(reg)
    nfa = delete_empty_edges(nfa)
    automaton = build_dfa(nfa)
    return automaton


def find_prefixes_in_automaton(automaton, string):
    t = 0
    i = 0
    for i in range(len(string)):
        if string[i] in automaton[t].keys():
            t = automaton[t][string[i]]
        else:
            break
    return i


def find_prefixes(regular_expression, string):
    automaton = build_automaton(regular_expression)
    return find_prefixes_in_automaton(automaton, string)


if __name__ == '__main__':
    alpha = input()
    u = input()
    print(find_prefixes(alpha, u))
