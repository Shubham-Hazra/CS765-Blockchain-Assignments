import random
from queue import PriorityQueue

from event import CreateTXN, Event, ReceiveTXN, MineBlock
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
        self.initialize_events()
        self.run(max_steps)

    def initialize_events(self):
        print(len(self.N.nodes))
        for node in self.N.nodes:
            self.events.put(CreateTXN(
                node.pid, node.pid, 0, self.transaction_delay()
            ))
            # Randomly choosing a node and starting the mining process
            self.events.put(MineBlock(
            node.pid, node.pid, 0, node.get_PoW_delay()
            ))
            # print(self.events.get())

    def transaction_delay(self):
        return random.expovariate(1 / self.Ttx)

    # The delay for mining is included in Node class
    # def block_delay(self):
    #     return random.expovariate(1 / self.I)

    def run(self, max_steps = 10000):
        step_count = 0
        while step_count <= max_steps:
            if not self.events.empty():
                # Executing other events
                current_event = self.events.get()
            else:
                print("Simulation Complete!!")
                break
            print("Step Count: ", step_count)
            current_event.addEvent(self.N, self)
            step_count+=1


# Test
S = Simulator(15, 10,10, 1000, 6, 1000)
# S.run(10)