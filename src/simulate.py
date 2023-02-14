import random
import sys
from queue import PriorityQueue

from treelib import Node, Tree

from block import Block
from event import CreateTXN, Event, ForwardBlock, MineBlock, ReceiveTXN
from network import Network


class Simulator:
    def __init__(self, n, z0,z1, Ttx, I, max_steps=100000):
        self.N = Network(n,z0,z1,I)
        self.z0 = z0 # Percentage of slow nodes
        self.z1 = z1 # Percentage of low CPU nodes
        self.Ttx = Ttx # Mean transaction interarrival time
        self.I = I # Mean block interarrival time
        self.txn_id = 0
        self.block_id = 1
        self.mining_txn_id = -1
        self.num_min_events = 0
        self.events = PriorityQueue()
        self.global_transactions = {} # To store th TXN objet indexed by the unique ID of the TXN
        self.curr_time = 0 # Stores the timestamp of the current event being run
        self.initialize_events()
        self.run(max_steps)
        self.print_blockchains()
        self.visualize()
        
    # VERIFIED
    def initialize_events(self):
        print(len(self.N.nodes))
        for node in self.N.nodes[0:5]:
            self.events.put(CreateTXN(
                node.pid, node.pid, 0, self.transaction_delay()
            ))
        # nodes_to_mine = random.sample(self.N.nodes,5) # HYPERPARAMETER HERE TO TUNE
         
        for node in self.N.nodes[0:1]:
            # Randomly choosing a node and starting the mining process
            # self.num_min_events+=1
            PoW_delay = node.get_PoW_delay()
            block = Block(node.pid, "Block_0", PoW_delay,[], self.N.num_nodes,[100]*self.N.num_nodes, self.block_id,1 )
            self.block_id+=1
            self.events.put(ForwardBlock(block, node.pid, node.pid, 0, PoW_delay))
        # print(self.events)
        # sorted_list = [] 
        # while self.events.empty()  == False:
        #     sorted_list.append(self.events.get())
        # print(sorted_list)
        # sys.exit(0)
    
    # VERIFIED
    def transaction_delay(self):
        return random.expovariate(1 / self.Ttx)
    
    # VERIFIED
    def run(self, max_steps = 10000):
        step_count = 0
        while step_count <= max_steps:
            if not self.events.empty():
                # Executing other events
                current_event = self.events.get()
                self.curr_time = current_event.run_time
            # elif self.events.empty() and step_count <= max_steps:
            #     node_list = random.sample(self.N.nodes,1)[0:6]
            #     for node in node_list:
            #         if random.random() > 0.85:
            #             self.events.put(CreateTXN(
            #             node.pid, node.pid, self.curr_time, self.curr_time + self.transaction_delay()
            #             ))
            #         else:
            #             # Randomly choosing a node and starting the mining process
            #             # self.events.put(MineBlock(
            #             # node.pid, node.pid, self.curr_time, self.curr_time + node.get_PoW_delay()
            #             # ))
            #             PoW_delay = node.get_PoW_delay()
            #             block = Block(node.pid, "Block_0", PoW_delay,[], self.N.num_nodes,[100]*self.N.num_nodes, self.block_id,1 )
            #             self.block_id+=1
            #             self.events.put(ForwardBlock(block, node.pid, node.pid, 0, PoW_delay))
            #     current_event = self.events.get()
            #     self.curr_time = current_event.run_time
            else:
                print("Simulation Complete!!")
                break
            print("Step Count: ", step_count)
            current_event.addEvent(self.N, self)
            step_count+=1

    # VERIFIED
    def print_blockchains(self):
        for node in self.N.nodes[0:6]:
            node.print_blockchain()

    # VERIFIED
    def visualize(self):
        tree = Tree()
        node = self.N.nodes[0]
        tree.create_node("Block_0", "Block_0")
        for block in node.blockchain_tree.keys():
            if block == "Block_0":
                continue
            tree.create_node(block,block, parent = node.blockchain_tree[block]['parent'])
        tree.show()


# Test
if __name__ == "__main__":
    S = Simulator(100, 10, 30, 1000, 6, 10000)
# S.run(10)
# node = random.sample(self.N.nodes,1)[0]
# if random.random() > 0.8:
#     self.events.put(CreateTXN(
#     node.pid, node.pid, 0, self.transaction_delay()
#     ))
# else:
#     # Randomly choosing a node and starting the mining process
#     self.events.put(MineBlock(
#     node.pid, node.pid, 0, node.get_PoW_delay()
#     ))

# elif self.num_min_events == 0 and step_count <= max_steps:
# node_list = random.sample(self.N.nodes,1)[0:6]
# for node in node_list:
#     if random.random() > 0.95:
#         self.events.put(CreateTXN(
#         node.pid, node.pid, 0, self.transaction_delay()
#         ))
#     else:
#         # Randomly choosing a node and starting the mining process
#         self.events.put(MineBlock(
#         node.pid, node.pid, 0, node.get_PoW_delay()
#         ))
# current_event = self.events.get()
