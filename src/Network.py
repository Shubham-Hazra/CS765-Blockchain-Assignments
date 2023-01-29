import networkx as nx
import random 

class Network:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes; # Number of nodes in theconnected graph
        self.create_graph() # create the P2P Network
    
    def create_graph(self):
        sequence = [random.randint(4,8) for i in range(self.num_nodes)] # Each node is connected to 4 to 8 peers
        sequence.sort()
        print(sequence)
        G = nx.random_degree_sequence_graph(sequence, seed=42)
        print(sorted(d for n, d in G.degree()))

# Testing the class
N = Network(10)