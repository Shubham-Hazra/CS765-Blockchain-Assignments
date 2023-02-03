import threading
import collections
from queue import Queue

class Node(threading.Thread):
    def __init__(self, pid, attrb, gen_block):
        threading.Thread.__init__(self)
        self.pid = pid # Unique Id of the peer
        self.cpu = attrb['cpu'] # CPU speed of the peer
        self.speed = attrb['speed'] # Speed of the peer
        self.peers = {} # Storing the pointer for function to put events in Queues of peers

        self.semaphore = threading.Semaphore(0)
        self.queue = Queue() # Queue of events put by the peers or the node itself 
        self.event_buffer = collections.defaultdict(set) # Event buffer - which receives events received and forwards it to its peers

        # Initialize the blockchain
        #  self.blockchain = BlockChain(gen_block, self.pid)
        # self.block_timer = None
        # # the random no denotes the computation power of the peer. lower the random no, higher the comp. power.
        # self.block_gen_mean = Parameters.block_gen_mean * (random.uniform(0.5, 1.0))
    
    # receives the pointer of the neighbor's enqueue function from the Network class and puts it in his list - 
    # so that it can communicate anything by putting events in the neighbour's queue
    def add_peer_pointer(self, pid, receive_event_function):
        self.peers[pid] = receive_event_function

    # This is the function that every neighbour of this node has a pointer to and will use that to put
    # events in this node's queue - which will execute after the assigned time - to simulate delays
    def receive_event(self, event):
        print("Debug")
        self.queue.put(event)
        self.semaphore.release()

    # To generate TXNs, with exponential distribution
    def generate_trans(self):
        pass

    # Debugging the function pointer list
    def print_funct_points(self):
        print (self.peers)

N = Node(1, {"cpu": "low", "speed": "high"},2)
print(N.peers)