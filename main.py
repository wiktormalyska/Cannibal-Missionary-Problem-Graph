from pyvis.network import Network


class Node:

    def __init__(self, cannibal_left, cannibal_right, missionary_left, missionary_right, boat_pos):
        self.cannibal_left = cannibal_left
        self.cannibal_right = cannibal_right
        self.missionary_left = missionary_left
        self.missionary_right = missionary_right
        self.boat_pos = boat_pos
        self.index = 0

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
        label = ('KL: ' + str(self.cannibal_left) + ' '
                 + 'KR: ' + str(self.cannibal_right) + '\n '
                 + 'ML: ' + str(self.missionary_left) + ' '
                 + 'MR: ' + str(self.missionary_right) + '\n '
                 + 'B: ' + str(self.boat_pos))
        return label


class Edge:
    def __init__(self, node1, node2, instruction):
        self.node1: Node = node1
        self.node2: Node = node2
        self.instruction = instruction


class Graph:
    def __init__(self):
        self.edges = []
        self.nodes = set()
     #   self.visited_nodes = set()
        self.node_index = 0

    def print_graph(self):
        for edge in self.edges:
            # print(edge.node1.get_as_label(), '\n->\n', edge.node2.get_as_label(), '\ninstruction:', edge.instruction, '\n')
            print(edge.node1.index, '->', edge.node2.index, 'instruction:', edge.instruction, '\n')

    def add_node(self, current_node):
  #      if current_node not in self.visited_nodes:
            if current_node.cannibal_left + current_node.cannibal_right > 3 or current_node.missionary_left + current_node.missionary_right > 3:
                return
            current_node.index = self.node_index
            self.node_index += 1
            #self.visited_nodes.add(current_node)
            self.nodes.add(current_node)
            self.check_connections(current_node)

    def add_edge(self, node1, node2, instruction_number):
        if node2 not in self.nodes:
            self.add_node(node2)
        self.edges.append(Edge(node1, node2, instruction_number))

    def check_connections(self, current_node):
        self.cannibal_to_right(current_node)
        self.cannibal_to_left(current_node)
        self.duo_cannibal_to_right(current_node)
        self.duo_cannibal_to_left(current_node)
        self.missionary_to_right(current_node)
        self.missionary_to_left(current_node)
        self.duo_missionary_to_right(current_node)
        self.duo_missionary_to_left(current_node)
        self.missionary_and_cannibal_to_right(current_node)
        self.missionary_and_cannibal_to_left(current_node)

    # warunki:

    def cannibal_to_right(self, current_node):
        is_cannibal_on_left = current_node.cannibal_left >= 1
        is_enough_missionary_on_right = current_node.missionary_right >= current_node.cannibal_right + 1 or current_node.missionary_right == 0
        is_boat_on_left = current_node.boat_pos == 0
        if is_cannibal_on_left and is_enough_missionary_on_right and is_boat_on_left:
            new_node = Node(
                current_node.cannibal_left - 1,
                current_node.cannibal_right + 1,
                current_node.missionary_left,
                current_node.missionary_right,
                1)
            self.add_edge(current_node, new_node, 1)

    def cannibal_to_left(self, current_node):
        if (current_node.cannibal_right >= 1
                and (
                        current_node.missionary_left >= current_node.cannibal_left + 1 or current_node.missionary_left == 0)
                and current_node.boat_pos == 1):
            new_node = Node(
                current_node.cannibal_left + 1,
                current_node.cannibal_right - 1,
                current_node.missionary_left,
                current_node.missionary_right,
                0)
            self.add_edge(current_node, new_node, 2)

    def duo_cannibal_to_right(self, current_node):
        if (current_node.cannibal_left >= 2
                and (
                        current_node.missionary_right >= current_node.cannibal_right + 2 or current_node.missionary_right == 0)
                and current_node.boat_pos == 0):
            new_node = Node(
                current_node.cannibal_left - 2,
                current_node.cannibal_right + 2,
                current_node.missionary_left,
                current_node.missionary_right,
                1)
            self.add_edge(current_node, new_node, 3)

    def duo_cannibal_to_left(self, current_node):
        if (current_node.cannibal_right >= 2
                and (
                        current_node.missionary_left >= current_node.cannibal_left + 2 or current_node.missionary_left == 0)
                and current_node.boat_pos == 1):
            new_node = Node(
                current_node.cannibal_left + 2,
                current_node.cannibal_right - 2,
                current_node.missionary_left,
                current_node.missionary_right,
                0)
            self.add_edge(current_node, new_node, 4)

    def missionary_to_right(self, current_node):
        if (current_node.missionary_left >= 1
                and (
                        current_node.missionary_left - 1 >= current_node.cannibal_left or current_node.missionary_left - 1 == 0)
                and current_node.cannibal_right <= current_node.missionary_right + 1
                and current_node.boat_pos == 0):
            new_node = Node(
                current_node.cannibal_left,
                current_node.cannibal_right,
                current_node.missionary_left - 1,
                current_node.missionary_right + 1,
                1)
            self.add_edge(current_node, new_node, 5)

    def missionary_to_left(self, current_node):
        if (current_node.missionary_right >= 1
                and (
                        current_node.missionary_right - 1 >= current_node.cannibal_right or current_node.cannibal_right == 1)
                and current_node.cannibal_left <= current_node.missionary_left + 1
                and current_node.boat_pos == 1):
            new_node = Node(
                current_node.cannibal_left,
                current_node.cannibal_right,
                current_node.missionary_left + 1,
                current_node.missionary_right - 1,
                0)
            self.add_edge(current_node, new_node, 6)

    def duo_missionary_to_right(self, current_node):
        if (current_node.missionary_left >= 2
                and current_node.missionary_left - 2 >= current_node.cannibal_left
                and current_node.missionary_right + 2 >= current_node.cannibal_right
                and current_node.boat_pos == 0):
            new_node = Node(
                current_node.cannibal_left,
                current_node.cannibal_right,
                current_node.missionary_left - 2,
                current_node.missionary_right + 2,
                1)
            self.add_edge(current_node, new_node, 7)

    def duo_missionary_to_left(self, current_node):
        if (current_node.missionary_right >= 2
                and current_node.missionary_right - 2 >= current_node.cannibal_right
                and current_node.missionary_left + 2 >= current_node.cannibal_left
                and current_node.boat_pos == 1):
            new_node = Node(
                current_node.cannibal_left,
                current_node.cannibal_right,
                current_node.missionary_left + 2,
                current_node.missionary_right - 2,
                0)
            self.add_edge(current_node, new_node, 8)

    def missionary_and_cannibal_to_right(self, current_node):
        if (current_node.missionary_left >= 1
                and current_node.cannibal_left >= 1
                and current_node.boat_pos == 0):
            new_node = Node(
                current_node.cannibal_left - 1,
                current_node.cannibal_right + 1,
                current_node.missionary_left - 1,
                current_node.missionary_right + 1,
                1)
            self.add_edge(current_node, new_node, 9)

    def missionary_and_cannibal_to_left(self, current_node):
        if (current_node.missionary_right >= 1
                and current_node.cannibal_right >= 1
                and current_node.boat_pos == 1):
            new_node = Node(
                current_node.cannibal_left + 1,
                current_node.cannibal_right - 1,
                current_node.missionary_left + 1,
                current_node.missionary_right - 1,
                0)
            self.add_edge(current_node, new_node, 10)


graph = Graph()
graph.add_node(Node(3, 0, 3, 0, 0))
graph.print_graph()
network = Network(directed=True)
for node in graph.nodes:
    network.add_node(node.index, label=node.get_as_label(), title=str(node.index))
for edge in graph.edges:
    network.add_edge(edge.node1.index, edge.node2.index, label=str(edge.instruction))

network.set_edge_smooth('dynamic')
network.toggle_physics(True)
network.show_buttons(filter_=['physics'])
network.show("graph.html", local=True, notebook=False)
