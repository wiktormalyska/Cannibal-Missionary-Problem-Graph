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
        if node not in self.nodes:
            self.nodes.add(node)
            self.check_connections(node)

    def check_connections(self, node):
        if self.cannibal_to_right(node):
            self.index += 1
            new_node = Node(self.index,
                            node.cannibal_left - 1,
                            node.cannibal_right + 1,
                            node.missionary_left,
                            node.missionary_right,
                            'right')
            self.add_node(new_node)
            if not any(edge.node1 == node and edge.node2 == new_node for edge in self.edges):
                self.edges.append(Edge(node, new_node, 1))
        self.cannibal_to_left(node)
        self.duo_cannibal_to_right(node)
        self.duo_cannibal_to_left(node)
        self.missionary_to_right(node)
        self.missionary_to_left(node)
        self.duo_missionary_to_right(node)
        self.duo_missionary_to_left(node)
        self.missionary_and_cannibal_to_right(node)
        self.missionary_and_cannibal_to_left(node)

    # warunki:

    def cannibal_to_right(self, node):
        if (node.cannibal_left >= 1
                and (node.missionary_right >= node.cannibal_right + 1 or node.missionary_right == 0)
                and node.boat_pos == 'left'):
            return True
        return False


    def cannibal_to_left(self, node):
        if (node.cannibal_right >= 1
                and (node.missionary_left >= node.cannibal_left + 1 or node.missionary_left == 0)
                and node.boat_pos == 'right'):
            self.index += 1
            new_node = Node(self.index,
                            node.cannibal_left + 1,
                            node.cannibal_right - 1,
                            node.missionary_left,
                            node.missionary_right,
                            'left')
            self.add_node(new_node)
            if not any(edge.node1 == node and edge.node2 == new_node for edge in self.edges):
                self.edges.append(Edge(node, new_node, 2))

    def duo_cannibal_to_right(self, node):
        if (node.cannibal_left >= 2
                and (node.missionary_right >= node.cannibal_right + 2 or node.missionary_right == 0)
                and node.boat_pos == 'left'):
            self.index += 1
            new_node = Node(self.index,
                            node.cannibal_left - 2,
                            node.cannibal_right + 2,
                            node.missionary_left,
                            node.missionary_right,
                            'right')
            self.add_node(new_node)
            if not any(edge.node1 == node and edge.node2 == new_node for edge in self.edges):
                self.edges.append(Edge(node, new_node, 3))

    def duo_cannibal_to_left(self, node):
        if (node.cannibal_right >= 2
                and (node.missionary_left >= node.cannibal_left + 2 or node.missionary_left == 0)
                and node.boat_pos == 'right'):
            self.index += 1
            new_node = Node(self.index,
                            node.cannibal_left + 2,
                            node.cannibal_right - 2,
                            node.missionary_left,
                            node.missionary_right,
                            'left')
            self.add_node(new_node)
            if not any(edge.node1 == node and edge.node2 == new_node for edge in self.edges):
                self.edges.append(Edge(node, new_node, 4))

    def missionary_to_right(self, node):
        if (node.missionary_left >= 1
                and (node.missionary_left - 1 >= node.cannibal_left or node.cannibal_left == 1)
                and node.boat_pos == 'left'):
            self.index += 1
            new_node = Node(self.index,
                            node.cannibal_left,
                            node.cannibal_right,
                            node.missionary_left - 1,
                            node.missionary_right + 1,
                            'right')
            self.add_node(new_node)
            if not any(edge.node1 == node and edge.node2 == new_node for edge in self.edges):
                self.edges.append(Edge(node, new_node, 5))

    def missionary_to_left(self, node):
        if (node.missionary_right >= 1
                and (node.missionary_right - 1 >= node.cannibal_right or node.cannibal_right == 1)
                and node.boat_pos == 'right'):
            self.index += 1
            new_node = Node(self.index,
                            node.cannibal_left,
                            node.cannibal_right,
                            node.missionary_left + 1,
                            node.missionary_right - 1,
                            'left')
            self.add_node(new_node)
            if not any(edge.node1 == node and edge.node2 == new_node for edge in self.edges):
                self.edges.append(Edge(node, new_node, 6))

    def duo_missionary_to_right(self, node):
        if (node.missionary_left >= 2
                and node.missionary_left - 2 >= node.cannibal_left
                and node.missionary_right + 2 >= node.cannibal_right
                and node.boat_pos == 'left'):
            self.index += 1
            new_node = Node(self.index,
                            node.cannibal_left,
                            node.cannibal_right,
                            node.missionary_left - 2,
                            node.missionary_right + 2,
                            'right')
            self.add_node(new_node)
            if not any(edge.node1 == node and edge.node2 == new_node for edge in self.edges):
                self.edges.append(Edge(node, new_node, 7))

    def duo_missionary_to_left(self, node):
        if (node.missionary_right >= 2
                and node.missionary_right - 2 >= node.cannibal_right
                and node.missionary_left + 2 >= node.cannibal_left
                and node.boat_pos == 'right'):
            self.index += 1
            new_node = Node(self.index,
                            node.cannibal_left,
                            node.cannibal_right,
                            node.missionary_left + 2,
                            node.missionary_right - 2,
                            'left')
            self.add_node(new_node)
            if not any(edge.node1 == node and edge.node2 == new_node for edge in self.edges):
                self.edges.append(Edge(node, new_node, 8))

    def missionary_and_cannibal_to_right(self, node):
        if (node.missionary_left >= 1
                and node.cannibal_left >= 1
                and node.boat_pos == 'left'):
            self.index += 1
            new_node = Node(self.index,
                            node.missionary_left - 1,
                            node.cannibal_right + 1,
                            node.missionary_left - 1,
                            node.missionary_right + 1,
                            'right')
            self.add_node(new_node)
            if not any(edge.node1 == node and edge.node2 == new_node for edge in self.edges):
                self.edges.append(Edge(node, new_node, 9))

    def missionary_and_cannibal_to_left(self, node):
        if (node.missionary_right >= 1
                and node.cannibal_right >= 1
                and node.boat_pos == 'right'):
            self.index += 1
            new_node = Node(self.index,
                            node.missionary_left + 1,
                            node.cannibal_right - 1,
                            node.missionary_left + 1,
                            node.missionary_right - 1,
                            'left')
            self.add_node(new_node)
            if not any(edge.node1 == node and edge.node2 == new_node for edge in self.edges):
                self.edges.append(Edge(node, new_node, 10))


graph = Graph()
network = Network()
for node in graph.nodes:
    network.add_node(node.index, label=node.get_as_label())
for edge in graph.edges:
    network.add_edge(edge.node1.index, edge.node2.index, label=str(edge.instruction))

network.toggle_physics(True)
network.show("graph.html", local=True, notebook=False)
