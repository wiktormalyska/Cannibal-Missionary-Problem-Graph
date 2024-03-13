from pyvis.network import Network


class Node:
    def __init__(self, index, cannibal_left, cannibal_right, missionary_left, missionary_right, boat_pos):
        self.index = index
        self.cannibal_left = cannibal_left
        self.cannibal_right = cannibal_right
        self.missionary_left = missionary_left
        self.missionary_right = missionary_right
        self.boat_pos = boat_pos

    def __eq__(self, other):
        return (self.cannibal_left == other.cannibal_left and
                self.cannibal_right == other.cannibal_right and
                self.missionary_left == other.missionary_left and
                self.missionary_right == other.missionary_right and
                self.boat_pos == other.boat_pos)

    def __hash__(self):
        return hash((self.cannibal_left, self.cannibal_right,
                     self.missionary_left, self.missionary_right, self.boat_pos))

    def get_as_label(self):
        label = (str(self.cannibal_left) + ' '
                 + str(self.cannibal_right) + '\n '
                 + str(self.missionary_left) + ' '
                 + str(self.missionary_right) + '\n '
                 + str(self.boat_pos))
        return label


class Edge:
    def __init__(self, node1, node2, instruction):
        self.node1 = node1
        self.node2 = node2
        self.instruction = instruction


class Graph:
    def __init__(self):
        self.edges = []
        self.nodes = set()
        self.index = 0
        start_node = Node(0, 3, 0, 3, 0, 'left')
        self.add_node(start_node)

    def add_node(self, node):
        self.check_connections(node)

    def check_connections(self, node):
        self.cannibal_to_right(node)
        self.cannibal_to_left(node)
        self.duo_cannibal_to_right(node)
        self.duo_cannibal_to_left(node)
        self.missionary_to_right(node)
        self.missionary_to_left(node)
        self.duo_missionary_to_right(node)
        self.duo_missionary_to_left(node)
        self.missionary_and_cannibal_to_right(node)
        self.missionary_and_cannibal_to_left(node)

    def add_edge(self, node1, node2, instruction_number):
        if node2 not in self.nodes:
            self.add_node(node2)
            self.edges.append(Edge(node1, node2, instruction_number))
        else:
            self.edges.append(Edge(node1, node2, instruction_number))

    # warunki:

    def cannibal_to_right(self, current_node):
        if (current_node.cannibal_left >= 1
                and (current_node.missionary_right >= current_node.cannibal_right + 1 or current_node.missionary_right == 0)
                and current_node.boat_pos == 'left'):
            self.index += 1
            new_node = Node(self.index,
                            current_node.cannibal_left - 1,
                            current_node.cannibal_right + 1,
                            current_node.missionary_left,
                            current_node.missionary_right,
                            'right')
            self.add_edge(current_node, new_node, 1)

    def cannibal_to_left(self, current_node):
        if (current_node.cannibal_right >= 1
                and (
                        current_node.missionary_left >= current_node.cannibal_left + 1 or current_node.missionary_left == 0)
                and current_node.boat_pos == 'right'):
            self.index += 1
            new_node = Node(self.index,
                            current_node.cannibal_left + 1,
                            current_node.cannibal_right - 1,
                            current_node.missionary_left,
                            current_node.missionary_right,
                            'left')
            self.add_edge(current_node, new_node, 2)

    def duo_cannibal_to_right(self, current_node):
        if (current_node.cannibal_left >= 2
                and (
                        current_node.missionary_right >= current_node.cannibal_right + 2 or current_node.missionary_right == 0)
                and current_node.boat_pos == 'left'):
            self.index += 1
            new_node = Node(self.index,
                            current_node.cannibal_left - 2,
                            current_node.cannibal_right + 2,
                            current_node.missionary_left,
                            current_node.missionary_right,
                            'right')
            self.add_edge(current_node, new_node, 3)

    def duo_cannibal_to_left(self, current_node):
        if (current_node.cannibal_right >= 2
                and (
                        current_node.missionary_left >= current_node.cannibal_left + 2 or current_node.missionary_left == 0)
                and current_node.boat_pos == 'right'):
            self.index += 1
            new_node = Node(self.index,
                            current_node.cannibal_left + 2,
                            current_node.cannibal_right - 2,
                            current_node.missionary_left,
                            current_node.missionary_right,
                            'left')
            self.add_edge(current_node, new_node, 4)

    def missionary_to_right(self, current_node):
        if (current_node.missionary_left >= 1
                and (current_node.missionary_left - 1 >= current_node.cannibal_left or current_node.cannibal_left == 1)
                and current_node.boat_pos == 'left'):
            self.index += 1
            new_node = Node(self.index,
                            current_node.cannibal_left,
                            current_node.cannibal_right,
                            current_node.missionary_left - 1,
                            current_node.missionary_right + 1,
                            'right')
            self.add_edge(current_node, new_node, 5)

    def missionary_to_left(self, current_node):
        if (current_node.missionary_right >= 1
                and (
                        current_node.missionary_right - 1 >= current_node.cannibal_right or current_node.cannibal_right == 1)
                and current_node.boat_pos == 'right'):
            self.index += 1
            new_node = Node(self.index,
                            current_node.cannibal_left,
                            current_node.cannibal_right,
                            current_node.missionary_left + 1,
                            current_node.missionary_right - 1,
                            'left')
            self.add_edge(current_node, new_node, 6)

    def duo_missionary_to_right(self, current_node):
        if (current_node.missionary_left >= 2
                and current_node.missionary_left - 2 >= current_node.cannibal_left
                and current_node.missionary_right + 2 >= current_node.cannibal_right
                and current_node.boat_pos == 'left'):
            self.index += 1
            new_node = Node(self.index,
                            current_node.cannibal_left,
                            current_node.cannibal_right,
                            current_node.missionary_left - 2,
                            current_node.missionary_right + 2,
                            'right')
            self.add_edge(current_node, new_node, 7)
    def duo_missionary_to_left(self, current_node):
        if (current_node.missionary_right >= 2
                and current_node.missionary_right - 2 >= current_node.cannibal_right
                and current_node.missionary_left + 2 >= current_node.cannibal_left
                and current_node.boat_pos == 'right'):
            self.index += 1
            new_node = Node(self.index,
                            current_node.cannibal_left,
                            current_node.cannibal_right,
                            current_node.missionary_left + 2,
                            current_node.missionary_right - 2,
                            'left')
            self.add_edge(current_node, new_node, 8)

    def missionary_and_cannibal_to_right(self, current_node):
        if (current_node.missionary_left >= 1
                and current_node.cannibal_left >= 1
                and current_node.boat_pos == 'left'):
            self.index += 1
            new_node = Node(self.index,
                            current_node.missionary_left - 1,
                            current_node.cannibal_right + 1,
                            current_node.missionary_left - 1,
                            current_node.missionary_right + 1,
                            'right')
            self.add_edge(current_node, new_node, 9)

    def missionary_and_cannibal_to_left(self, current_node):
        if (current_node.missionary_right >= 1
                and current_node.cannibal_right >= 1
                and current_node.boat_pos == 'right'):
            self.index += 1
            new_node = Node(self.index,
                            current_node.missionary_left + 1,
                            current_node.cannibal_right - 1,
                            current_node.missionary_left + 1,
                            current_node.missionary_right - 1,
                            'left')
            self.add_edge(current_node, new_node, 10)


graph = Graph()
network = Network()
for node in graph.nodes:
    network.add_node(node.index, label=node.get_as_label())
for edge in graph.edges:
    network.add_edge(edge.node1.index, edge.node2.index, label=str(edge.instruction))

network.toggle_physics(True)
network.show("graph.html", local=True, notebook=False)
