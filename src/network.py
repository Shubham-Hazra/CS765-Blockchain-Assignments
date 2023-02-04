import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from node import Node


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
        self.set_latency_attrb() # Sets the latency of the network
        self.set_attrb()

        self.nodes = [Node(i, self.attrb[i], 0, 100) for i in range(self.num_nodes)] # Array of Node objects which have operations defined in them 
        # By default everyone has 100 BTC at the start

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

            if nx.is_connected(self.G) and min([val for (node, val) in self.G.degree()]) >= 3:
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
    
    def set_latency_attrb(self):  # Sets the latency of the network
        for edge in self.G.edges:
            node1 = edge[0]
            node2 = edge[1]
            # Minimum latency between two nodes is 10ms and maximum is 500ms due to the speed of light
            min_latency = np.random.uniform(10, 500)/1000  # in seconds
            self.G[node1][node2]['l'] = min_latency
            if self.attrb[node1]['speed'] == 'low' or self.attrb[node2]['speed'] == 'low':
                self.G[node1][node2]['c'] = 5 # Link speed is 5Mbps if either of the nodes has low speed
            else:
                self.G[node1][node2]['c'] = 100 # Link speed is 100Mbps if both of the nodes have high speed
            d = 96/(self.G[node1][node2]['c']*1000) + np.random.exponential()  # Queueing delay at node 1
            self.G[node1][node2]['d'] = d

    def calc_latency(self, node1, node2, packet_size):
        return self.G[node1][node2]['l'] + packet_size/self.G[node1][node2]['c'] + self.G[node1][node2]['d']
        
        
    def get_latency(self, node1, node2, m): # Returns the latency between two nodes (m is the size of the message in Mbs)
        return self.G[node1][node2]['l'] + self.G[node1][node2]['d'] + m/self.G[node1][node2]['c']



# Testing the class
# N = Network(15)
# print("CPU power of first node" , N.G.nodes[0]['cpu'])
# N.show_graph()
# for edge in N.G.edges:
#     print("Latency between the nodes of the first edge (in seconds): ", N.get_latency(edge[0],edge[1],17))
#     break
# Debug for node bein able to use the peers' receive_event() function which will put events in the peers' queue
# for i in range(N.num_nodes):
#     for j in N.G.neighbors(i):  
#         N.nodes[i].peers[j](10)







 # def start_nodes(self): # Start the thread for each Node
    #     for i in self.nodes:
    #         i.start()

    # def connect_peers(self):
    #     for i in range(self.num_nodes):
    #         peers = self.G.neighbors(i)
    #         for j in peers:
    #             self.nodes[i].add_peer_pointer(self.nodes[j].pid, self.nodes[j].receive_event)



