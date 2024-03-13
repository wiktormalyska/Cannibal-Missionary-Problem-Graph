from pyvis.network import Network
network = Network()
network.add_node(0)
network.add_node(1)
network.add_edge(0,1)
network.show("basic.html", local=True, notebook=False)