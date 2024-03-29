import sys

from pyvis.network import Network
from collections import deque


class Edge:
    def __init__(self, from_node, to_node, instruction):
        self.node1 = from_node
        self.node2 = to_node
        self.instruction = instruction


class Node:
    def __init__(self, cl, cr, ml, mr, boat, color, is_end):
        self.cl = cl
        self.cr = cr
        self.ml = ml
        self.mr = mr
        self.boat: bool = boat
        self.index = self.get_index()
        self.color: str = color
        self.is_end: bool = is_end

    def get_index(self):
        boat = 1 if self.boat else 0
        return str(self.cl) + str(self.cr) + str(self.ml) + str(self.mr) + str(boat)

    def get_label(self):
        if not self.boat:
            return ("C:" + str(self.cl) + "\t|B|\tC:" + str(self.cr) + "\n"
                    + "M:" + str(self.ml) + "\t|B\t|\tM:" + str(self.mr) + "\n")
        else:
            return ("C:" + str(self.cl) + "\t|\tB|\tC:" + str(self.cr) + "\n"
                    + "M:" + str(self.ml) + "\t|\tB|\tM:" + str(self.mr) + "\n")


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.queue = deque()

    def nodes_contain(self, node: Node):
        for n in self.nodes:
            if n.index == node.index:
                return True
        return False

    def edges_contain(self, edge: Edge):
        for e in self.edges:
            if e.node1.index == edge.node1.index and e.node2.index == edge.node2.index:
                return True
        return False

    def add_node(self, node: Node):
        if not self.nodes_contain(node):
            self.nodes.append(node)
            self.queue.append(node)

    def process_queue(self):
        while self.queue:
            node = self.queue.popleft()
            if not node.is_end:
                self.check_connections(node)
    def check_connections(self, node: Node):
        self.cl_to_r(node)
        self.cr_to_l(node)
        self.ml_to_r(node)
        self.mr_to_l(node)
        self.kl2_to_r(node)
        self.kr2_to_l(node)
        self.ml2_to_r(node)
        self.mr2_to_l(node)
        self.kl_ml_to_r(node)
        self.kr_mr_to_l(node)
        graph.process_queue()

    def cl_to_r(self, node: Node):
        if node.boat is False and node.cl > 0:
            if node.mr >= node.cr + 1 or node.mr == 0:
                color = "#138025"
                is_end = False
            else:
                color = "#801313"
                is_end = True
            new_node = Node(node.cl - 1, node.cr + 1, node.ml, node.mr, True, color, is_end)
            if not self.nodes_contain(new_node):
                self.add_node(new_node)
            if not self.edges_contain(Edge(node, new_node, "1")):
                self.edges.append(Edge(node, new_node, "1"))

    def cr_to_l(self, node: Node):
        if node.boat is True and node.cr > 0:
            if node.ml >= node.cl + 1 or node.ml == 0:
                color = "#138025"
                is_end = False
            else:
                color = "#801313"
                is_end = True
            new_node = Node(node.cl + 1, node.cr - 1, node.ml, node.mr, False, color, is_end)
            if not self.nodes_contain(new_node):
                self.add_node(new_node)
            if not self.edges_contain(Edge(node, new_node, "2")):
                self.edges.append(Edge(node, new_node, "2"))

    def ml_to_r(self, node: Node):
        if node.boat is False and node.mr + 1 >= node.cr and node.ml > 0:
            if node.ml - 1 >= node.cl or node.ml == 1:
                color = "#138025"
                is_end = False
            else:
                color = "#801313"
                is_end = True
            new_node = Node(node.cl, node.cr, node.ml - 1, node.mr + 1, True, color, is_end)
            if new_node not in self.nodes:
                self.add_node(new_node)
            if not self.edges_contain(Edge(node, new_node, "3")):
                self.edges.append(Edge(node, new_node, "3"))

    def mr_to_l(self, node: Node):
        if node.boat is True and node.ml + 1 >= node.cl and node.mr > 0:
            if node.mr - 1 >= node.cr or node.mr == 1:
                color = "#138025"
                is_end = False
            else:
                color = "#801313"
                is_end = True
            new_node = Node(node.cl, node.cr, node.ml + 1, node.mr - 1, False, color, is_end)
            if new_node not in self.nodes:
                self.add_node(new_node)
            if not self.edges_contain(Edge(node, new_node, "4")):
                self.edges.append(Edge(node, new_node, "4"))

    def kl2_to_r(self, node: Node):
        if node.boat is False and node.cl > 1:
            if node.mr >= node.cr + 2 or node.mr == 0:
                color = "#138025"
                is_end = False
            else:
                color = "#801313"
                is_end = True
            new_node = Node(node.cl - 2, node.cr + 2, node.ml, node.mr, True, color, is_end)
            if not self.nodes_contain(new_node):
                self.add_node(new_node)
            if not self.edges_contain(Edge(node, new_node, "5")):
                self.edges.append(Edge(node, new_node, "5"))

    def kr2_to_l(self, node: Node):
        if node.boat is True and node.cr > 1:
            if node.ml >= node.cl + 2 or node.ml == 0:
                color = "#138025"
                is_end = False
            else:
                color = "#801313"
                is_end = True
            new_node = Node(node.cl + 2, node.cr - 2, node.ml, node.mr, False, color, is_end)
            if not self.nodes_contain(new_node):
                self.add_node(new_node)
            if not self.edges_contain(Edge(node, new_node, "6")):
                self.edges.append(Edge(node, new_node, "6"))

    def ml2_to_r(self, node: Node):
        if node.boat == False and node.mr + 2 >= node.cr and node.ml > 1:
            if node.ml - 2 >= node.cl or node.ml == 2:
                color = "#138025"
                is_end = False
            else:
                color = "#801313"
                is_end = True
            new_node = Node(node.cl, node.cr, node.ml - 2, node.mr + 2, True, color, is_end)
            if new_node not in self.nodes:
                self.add_node(new_node)
            if not self.edges_contain(Edge(node, new_node, "7")):
                self.edges.append(Edge(node, new_node, "7"))

    def mr2_to_l(self, node: Node):
        if node.boat == True and node.ml + 2 >= node.cl and node.mr > 1:
            if node.mr - 2 >= node.cr or node.mr == 2:
                color = "#138025"
                is_end = False
            else:
                color = "#801313"
                is_end = True
            new_node = Node(node.cl, node.cr, node.ml + 2, node.mr - 2, False, color, is_end)
            if new_node not in self.nodes:
                self.add_node(new_node)
            if not self.edges_contain(Edge(node, new_node, "8")):
                self.edges.append(Edge(node, new_node, "8"))

    def kl_ml_to_r(self, node: Node):
        if node.boat == False and node.cl > 0 and node.ml > 0:
            if node.cr + 1 <= node.mr + 1:
                color = "#138025"
                is_end = False
            else:
                color = "#801313"
                is_end = True
            new_node = Node(node.cl - 1, node.cr + 1, node.ml - 1, node.mr + 1, True, color, is_end)
            if not self.nodes_contain(new_node):
                self.add_node(new_node)
            if not self.edges_contain(Edge(node, new_node, "9")):
                self.edges.append(Edge(node, new_node, "9"))

    def kr_mr_to_l(self, node: Node):
        if node.boat == True and node.cr > 0 and node.mr > 0:
            if node.cl + 1 <= node.ml + 1:
                color = "#138025"
                is_end = False
            else:
                color = "#801313"
                is_end = True
            new_node = Node(node.cl + 1, node.cr - 1, node.ml + 1, node.mr - 1, False, color, is_end)
            if not self.nodes_contain(new_node):
                self.add_node(new_node)
            if not self.edges_contain(Edge(node, new_node, "10")):
                self.edges.append(Edge(node, new_node, "10"))

    def print_graph(self):
        for edge in self.edges:
            print(edge.node1.index, edge.node2.index, edge.instruction)


graph = Graph()
graph.add_node(Node(3, 0, 3, 0, False, '#136180', False))
graph.process_queue()
graph.print_graph()
network = Network(directed=True, width="100%", bgcolor="#222222", font_color="white", height="99vh")
for nodee in graph.nodes:
    if nodee.cl==0 and nodee.ml==0 and nodee.cr==3 and nodee.mr==3 and nodee.boat==True:
        nodee.color='#136180'
    network.add_node(nodee.index, label=str(nodee.get_label()), title=str(nodee.index), color=nodee.color)
for edgee in graph.edges:
    network.add_edge(edgee.node1.index, edgee.node2.index, label=str(edgee.instruction))

network.set_edge_smooth('dynamic')
network.toggle_physics(True)
#network.show_buttons(filter_=['physics'])
network.barnes_hut(gravity=-3000, central_gravity=0, spring_strength=0.5, damping=1, overlap=1)
network.show("index.html", local=True, notebook=False)
