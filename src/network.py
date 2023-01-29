import networkx as nx
import random 
import matplotlib.pyplot as plt

class Network:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes; # Number of nodes in theconnected graph
        self.G = nx.Graph() # Stores the graph of the network
        self.create_graph() # create the P2P Network
       
    
    def create_graph(self):
        self.G.add_nodes_from([i for i in range(self.num_nodes)])

        sequence = [random.randint(4,8) for i in range(self.num_nodes)] # Each node has 4 to 8 peers
        # Randomly generate a valid degree sequence
        while not nx.is_graphical(sequence, "hh"): # Check if the given degree sequence is valid 
            sequence = [random.randint(4,8) for i in range(self.num_nodes)]

        # Sort the degree sequence
        sequence.sort()
        curr_deg = [0 for i in range(self.num_nodes)] # Maintains the current degree of all the nodes

        # Connects the nodes of the graph
        for i in range(self.num_nodes-1, -1, -1):
            for j in range(i-1, -1, -1):
                if curr_deg[i] == sequence[i]:
                    break
                elif curr_deg[j] < sequence[j]:
                    self.G.add_edge(i,j)
                    curr_deg[i]+=1
                    curr_deg[j]+=1
        
        # Shuffle some nodes to introduce randomness
        nx.double_edge_swap(self.G, nswap=5, max_tries=10000, seed=None)

        
        # Print the degree sequence
        print(sequence)

        # Print the graph
        nx.draw(self.G, with_labels=True)
        plt.show()


# Testing the class
N = Network(20)



