import threading
import collections
from queue import Queue

class Node:
    def __init__(self, pid, attrb, gen_block, BTC):
        # threading.Thread.__init__(self)
        self.pid = pid # Unique Id of the peer
        self.cpu = attrb['cpu'] # CPU speed of the peer
        self.speed = attrb['speed'] # Speed of the peer
        self.peers = {} # Storing the pointer for function to put events in Queues of peers
        self.BTC =  BTC
        self.transactions = []
        self.blocks = {} # Stores the blockchain as seen by the node
        self.blocksReceiveTime = [] # Stores the list of time of arrival of blocks by other nodes - to check whether new block has been received between t_k and t_k + T_k (as written in the problem statement)

    # receives the pointer of the neighbor's enqueue function from the Network class and puts it in his list - 
    # so that it can communicate anything by putting events in the neighbour's queue
    def add_peer_pointer(self, pid, receive_event_function):
        self.peers[pid] = receive_event_function

    # Debugging the function pointer list
    def print_funct_points(self):
        print (self.peers)

    def remove_common_transactions(self, block_transactions):
        ####### IMPLEMENT THIS !!!!!!##########
        # removes common transactions between block_transaction list and self.transactions from self.transactions
        pass
        

N = Node(1, {"cpu": "low", "speed": "high"},2, 100)
print(N.peers)



# self.semaphore = threading.Semaphore(0)
# self.queue = Queue() # Queue of events put by the peers or the node itself 
# self.event_buffer = collections.defaultdict(set) # Event buffer - which receives events received and forwards it to its peers

# Initialize the blockchain
#  self.blockchain = BlockChain(gen_block, self.pid)
# self.block_timer = None
# # the random no denotes the computation power of the peer. lower the random no, higher the comp. power.
# self.block_gen_mean = Parameters.block_gen_mean * (random.uniform(0.5, 1.0))