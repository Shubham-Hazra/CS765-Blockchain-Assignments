import networkx as nx
import random 
import matplotlib.pyplot as plt

class Network:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes; # Number of nodes in theconnected graph
        self.G = nx.Graph() # Stores the graph of the network
        self.adj = {} # Stores the dictionary of lists for storing the graph of the network
        self.create_graph() # create the P2P Network

        self.attrb = {} # Dictionary which contain attributes of each node (CPU and Speed)
        for i in range(self.num_nodes): # Initialize the dictionary
            self.attrb[i] = {}

        self.calc_cpu(10) # IMPORTANT: CHANGE AFTERWARDS, FOR NOW HAS BEEN SET TO CONSTANT
        self.calc_speed(10) # IMPORTANT: CHANGE AFTERWARDS, FOR NOW HAS BEEN SET TO CONSTANT
        self.set_attrb()

    
    def create_graph(self):

        # Repeat while the graph is connected
        while True:
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
            nx.double_edge_swap(self.G, nswap=self.num_nodes/4, max_tries=1000, seed=None) # The number of swaps is a hyper parameter

            if nx.is_connected(self.G) and min([val for (node, val) in self.G.degree()]) >= 2:
                break
            else:
                self.G.clear()

        # Converts Graph to dictionary of lists
        self.adj = nx.to_dict_of_lists(self.G, nodelist=None)
        print(self.adj)

        # Print the degree sequence
        print(sequence)


    def show_graph(self):
        # Print the graph
        nx.draw(self.G, with_labels=True)
        plt.show()

    def calc_cpu(self, z): # Sets z percent of nodes as low CPU 
        z = int(z*self.num_nodes/100.0)
        low_cpu = [] # Maintains a list of nodes whose CPU is set to low

        while True:
            node = random.randint(0,self.num_nodes)
            if node not in low_cpu:
                low_cpu.append(node)
            if len(low_cpu) >= z:
                break
        
        for i in range(self.num_nodes):
            if i in low_cpu:
                self.attrb[i]['cpu'] = 'low'
            else:
                self.attrb[i]['cpu'] = "high"


    def calc_speed(self, z): # Sets z percent of nodes to low speed ("slow")
        z = int(z*self.num_nodes/100.0)
        low_speed = [] # Maintains a list of nodes whose CPU is set to low

        while True:
            node = random.randint(0,self.num_nodes)
            if node not in low_speed:
                low_speed.append(node)
            if len(low_speed) >= z:
                break
        
        for i in range(self.num_nodes):
            if i in low_speed:
                self.attrb[i]['speed'] = 'low'
            else:
                self.attrb[i]['speed'] = "high"


    def set_attrb(self): # Sets the cpu and speed of the node calculated before
        nx.set_node_attributes(self.G, self.attrb)


# Testing the class
N = Network(20)
print("CPU power of first node" , N.G.nodes[0]['cpu'])
N.show_graph()



