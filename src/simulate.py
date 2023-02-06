import random
from queue import PriorityQueue

from event import CreateTXN, Event, MineBlock, ReceiveTXN
from network import Network


class Simulator:
    def __init__(self, n, z0,z1, Ttx, I, max_steps):
        self.N = Network(n)
        self.z0 = z0 # Percentage of slow nodes
        self.z1 = z1 # Percentage of low CPU nodes
        self.Ttx = Ttx # Mean transaction interarrival time
        self.I = I # Mean block interarrival time
        self.txn_id = 0
        self.block_id = 1
        self.mining_txn_id = -1
        self.events = PriorityQueue()
        self.global_transactions = {} # To store th TXN objet indexed by the unique ID of the TXN
        self.initialize_events()
        self.run(max_steps)
        self.print_blockchains()

    def initialize_events(self):
        print(len(self.N.nodes))
        for node in self.N.nodes[:int(len(self.N.nodes)/2)]:
            self.events.put(CreateTXN(
                node.pid, node.pid, 0, self.transaction_delay()
            ))
        nodes_to_mine = random.sample(self.N.nodes,8)
         
        for node in nodes_to_mine:
            # Randomly choosing a node and starting the mining process
            self.events.put(MineBlock(
            node.pid, node.pid, 0, node.get_PoW_delay()
            ))

    def transaction_delay(self):
        return random.expovariate(1 / self.Ttx)

    def run(self, max_steps = 10000):
        step_count = 0
        while step_count <= max_steps:
            
            ############################################################################
            if not self.events.empty():
                # Executing other events
                current_event = self.events.get()
            elif self.events.empty() and step_count <= max_steps:
                node = random.sample(self.N.nodes,1)[0]
                if random.random() > 0.7:
                    self.events.put(CreateTXN(
                    node.pid, node.pid, 0, self.transaction_delay()
                    ))
                else:
                    # Randomly choosing a node and starting the mining process
                    self.events.put(MineBlock(
                    node.pid, node.pid, 0, node.get_PoW_delay()
                    ))
                current_event = self.events.get()
            else:
                print("Simulation Complete!!")
                break
            print("Step Count: ", step_count)
            current_event.addEvent(self.N, self)
            step_count+=1

    def print_blockchains(self):
        for node in self.N.nodes[0:6]:
            node.print_blockchain()


# Test
S = Simulator(100, 10, 10, 1000, 6, 100000)
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
