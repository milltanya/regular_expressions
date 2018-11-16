class Error(Exception):
    pass


class RPNError(Error):
    def __init__(self, regular_expression, message):
        self.regular_expression = regular_expression
        self.message = message


def build_automaton(reg):
    if reg is '':
        return [{}]
    """
    build NFA
    """
    stack = []
    vertices = []
    first_vertex = 0
    for i in range(len(reg)):
        if reg[i].isalpha() or reg[i] == '1':
            u = len(vertices)
            v = u + 1
            vertices.append([[reg[i], v]])
            vertices.append([])
            stack.append([u, v])
        else:
            if reg[i] == '.':
                if len(stack) < 2:
                    raise RPNError(reg, "Error in the Reverse Polish "
                                        "notation: . is a binary operation")
                second = stack.pop()
                first = stack.pop()
                vertices[first[1]].append(['1', second[0]])
                stack.append([first[0], second[1]])
            else:
                if reg[i] == '+':
                    if len(stack) < 2:
                        raise RPNError(reg, "Error in the Reverse Polish "
                                       "notation: + is a binary operation")
                    second = stack.pop()
                    first = stack.pop()
                    vertices[first[0]].append(['1', second[0]])
                    vertices[first[1]].append(['1', second[1]])
                    stack.append([first[0], second[1]])
                else:
                    if reg[i] == '*':
                        if len(stack) < 1:
                            raise RPNError(reg, "Error in the Reverse Polish "
                                           "notation: + is an unary operation")
                        last = stack.pop()
                        vertices[last[1]].append(['1', last[0]])
                        stack.append([last[0], last[0]])
                    else:
                        raise RPNError(reg, "Error in the Reverse Polish "
                                       "notation: unknown symbol")
    if len(stack) != 1:
        raise RPNError(reg, "Error in the Reverse Polish notation: more than "
                       "1 element in the stack at the end of the expression")
    """
    delete empty edges
    """
    for u in range(len(vertices)):
        i = 0
        while i < len(vertices[u]):
            edge = vertices[u][i]
            if edge[0] == '1':
                vertices[u].remove(edge)
                v = edge[1]
                if u != v:
                    if first_vertex == v:
                        first_vertex = u
                    vertices[u].extend(vertices[v])
                    vertices[v].clear()
                    for a in range(len(vertices)):
                        for b in range(len(vertices[a])):
                            if vertices[a][b][1] == v:
                                vertices[a][b][1] = u
            else:
                i += 1
    """
    build DFA
    """
    classes = [[first_vertex]]
    automaton = []
    i = 0
    while i < len(classes):
        edges = dict()
        for vertex in classes[i]:
            for edge in vertices[vertex]:
                if edge[0] not in edges.keys():
                    edges[edge[0]] = []
                if edge[1] not in edges[edge[0]]:
                    edges[edge[0]].append(edge[1])
        automaton.append(dict())
        for symbol in edges.keys():
            edges[symbol].sort()
            if edges[symbol] not in classes:
                classes.append(edges[symbol])
            number = classes.index(edges[symbol])
            automaton[i][symbol] = number
        i += 1
    return automaton


def find_prefixes_in_automaton(dfa, string):
    t = 0
    i = 0
    for i in range(len(string)):
        if string[i] in dfa[t].keys():
            t = dfa[t][string[i]]
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
