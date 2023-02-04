import collections
from queue import Queue

from block import *


class Node:
    def __init__(self, pid, attrb, BTC):

        self.pid = pid  # Unique Id of the peer
        self.cpu = attrb['cpu']  # CPU speed of the peer
        self.speed = attrb['speed']  # Speed of the peer
        self.peers = {}  # Storing the pointer for function to put events in Queues of peers
        self.BTC = BTC  # Initial BTC balance of the peer
        self.blockchain_tree = {"Block_0": {"parent": None}} # Blockchain tree of the peer
        self.blockchain = {"Block_0":Block(None,0,None,0,None,None)}  # Blockchain of the peer
        self.longest_chain = ["Block_0"] 
        self.max_len = 0 
        self.txn_list = []  # List of transactions that the peer has seen but not included in any block
        self.included_txn = []  # List of transactions that the peer has included in a block

    # receives the pointer of the neighbor's enqueue function from the Network class and puts it in his list -
    # so that it can communicate anything by putting events in the neighbour's queue
    def add_peer_pointer(self, pid, receive_event_function):
        self.peers[pid] = receive_event_function

    # Debugging the function pointer list
    def print_funct_points(self):
        print(self.peers)

    # Function to find the longest chain in the blockchain
    def find_longest_chain(self):
        longest_chain = []
        max_block_id = None
        for block_id,block in self.blockchain.items():
            if block.length == self.max_len: # Finding the block with the maximum length
                max_block_id = block_id
        while max_block_id != None: # Traversing backwards till the genesis block
            longest_chain.append(max_block_id)
            max_block_id = self.blockchain_tree[max_block_id]["parent"]
        return longest_chain[::-1]

    # Function to check if the block is valid
    # Assuming a global transaction list and a global balance list
    def validate_block(self, block):
        for txn in block.transactions:
            if txn in self.included_txn: # Checking if the transaction is already included in the blockchain
                return False
            else:
                return True # Assuming that a block is broadcasted only if the balances are non-negative and hence the block is valid
        
    # Function to add a block to the blockchain
    def add_block(self, block):
        if self.validate_block(block): # Checking if the block is valid
            self.blockchain[block.block_id] = block # Adding the block to the blockchain
            self.blockchain_tree[block.block_id] = {"parent": block.previous_id} # Adding the block to the blockchain tree
            self.blockchain[block.block_id].length = self.blockchain[self.blockchain_tree[block.block_id]["parent"]].length + 1 # Updating the length of the block
            self.included_txn.extend(block.transactions) # Adding the transactions to the list of included transactions
            self.remove_common_TXN(block) # Removing the transactions from the list of transactions that the peer has seen but not included in any block
            if self.blockchain[block.block_id].length > self.max_len: # Checking if the block is the longest block
                self.max_len = self.blockchain[block.block_id].length # Updating the length of the longest chain
                self.longest_chain = self.find_longest_chain() # Updating the longest chain
            print(f"{self.pid} says {block.block_id} is valid and added to the blockchain")
        else:
            print(f"{self.pid} says {block.block_id} is invalid")

    def add_txn(self, txn_id):
        self.txn_list.append(txn_id)

    def remove_common_TXN(self, block):
        for txn in block.transactions:
            if txn in self.txn_list:
                del self.txn_list[txn]

N = Node(1, {"cpu": "low", "speed": "high"}, 100)
print(N.peers)


# self.semaphore = threading.Semaphore(0)
# self.queue = Queue() # Queue of events put by the peers or the node itself
# self.event_buffer = collections.defaultdict(set) # Event buffer - which receives events received and forwards it to its peers

# Initialize the blockchain
#  self.blockchain = BlockChain(gen_block, self.pid)
# self.block_timer = None
# # the random no denotes the computation power of the peer. lower the random no, higher the comp. power.
# self.block_gen_mean = Parameters.block_gen_mean * (random.uniform(0.5, 1.0))
