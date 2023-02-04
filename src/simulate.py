from network import Network
from queue import PriorityQueue
from event import Event, CreateTXN, ReceiveTXN 
import random

class Simulator:
    def __init__(self, n, z, tm, bm, max_steps):
        self.N = Network(n)
        self.tm = tm # Mean transaction interarrival time
        self.tm = tm # Mean block interarrival time
        self.txn_id = 0
        self.events = PriorityQueue()
        self.initialize_events()
        self.run(max_steps)

    def initialize_events(self):
        print(len(self.N.nodes))
        for node in self.N.nodes:
            self.events.put(CreateTXN(
                node.pid, node.pid, 0, self.transaction_delay()
            ))
            # print(self.events.get())

    def transaction_delay(self):
        return random.expovariate(1 / self.tm)

    def run(self, max_steps = 10000):
        step_count = 0
        while step_count <= max_steps:
            if not self.events.empty():
                current_event = self.events.get()
            else:
                print("Simulation Complete!!")
                break
            print("Step Count: ", step_count)
            current_event.run(self.N, self)
            step_count+=1


# Test
S = Simulator(15, 10, 10, 10, 10000)
# S.run(10)