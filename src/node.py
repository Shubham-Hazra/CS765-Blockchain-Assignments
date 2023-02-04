import collections
import random
from queue import Queue

from treelib import Tree

from block import *
from event import *
from parameters import *


class Node:
    def __init__(self, pid, attrb, BTC):

        self.pid = pid  # Unique Id of the peer
        self.cpu = attrb['cpu']  # CPU speed of the peer
        self.hashing_power = attrb['hashing_power']  # Hashing power of the peer
        self.speed = attrb['speed']  # Speed of the peer
        self.peers = {}  # Storing the pointer for function to put events in Queues of peers
        self.BTC = BTC  # Initial BTC balance of the peer
        self.blockchain_tree = {"Block_0": {"parent": None}} # Blockchain tree of the peer
        self.blockchain = {"Block_0":Block(None,None,None,None,0,0)}  # Blockchain of the peer - stores the block objects, Initially the genesis block is added
        self.longest_chain = ["Block_0"] # Longest chain of the peer as a list of block ids
        self.max_len = 0  # Length of the longest chain
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
        if block.previous_id not in self.blockchain: # Checking if the previous block is in the blockchain
            return False
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
            self.blockchain[block.block_id].length = self.blockchain[block.previous_id].length + 1 # Updating the length of the block
            self.included_txn.extend(block.transactions) # Adding the transactions to the list of included transactions
            self.remove_common_TXN(block) # Removing the transactions from the list of transactions that the peer has seen but not included in any block
            if self.blockchain[block.block_id].length > self.max_len: # Checking if the block is the longest block
                self.max_len = self.blockchain[block.block_id].length # Updating the length of the longest chain
                self.longest_chain = self.find_longest_chain() # Updating the longest chain
            print(f"{self.pid} says {block.block_id} is valid and added to its blockchain")
        else:
            print(f"{self.pid} says {block.block_id} is invalid")

    def add_txn(self, txn_id): # Adding a transaction to the list of transactions that the peer has seen but not included in any block
        self.txn_list.append(txn_id)

    def remove_common_TXN(self, block): # Removing the transactions that are included in the block from the list of transactions that the peer has seen but not included in any block
        for txn in block.transactions:
            if txn in self.txn_list:
                del self.txn_list[txn]
    
    def mine_block(self):
        upper_limit = max(len(self.txn_list),999) # Upper limit of the number of transactions that can be included in the block
        num_txn_to_mine = random.randint(1,upper_limit) # Number of transactions to be included in the block
        txn_to_mine = random.sample(self.txn_list,num_txn_to_mine) # Transactions to be included in the block
        mining_time = I/self.hashing_power + random.expovariate(1) # Mining time of the block
        block = Block(self.pid, self.longest_chain[-1], CURRENT_TIME, txn_to_mine) # Creating the block
        mine = MineBlock(self.pid,self.pid, CURRENT_TIME, CURRENT_TIME + mining_time) # Creating the event
    

    
    def print_blockchain(self):
        added = set()
        tree = Tree()
        dict_ = self.blockchain_tree.copy()
        while dict_:  # while dict_ is not empty
            for key, value in dict_.items():
                if value['parent'] in added:
                    tree.create_node(key, key, parent=value['parent'])
                    added.add(key)
                    dict_.pop(key)
                    break
                elif value['parent'] is None:
                    tree.create_node(key, key)
                    added.add(key)
                    dict_.pop(key)
                    break
        tree.show()

N = Node(1, {"cpu": "low", "speed": "high","hashing_power" : 0.1}, 100)
N.add_block(Block(1, "Block_0", 0, ["txn_1", "txn_2"]))
N.add_block(Block(2, "Block_1", 1, ["txn_3", "txn_4"]))
N.add_block(Block(3, "Block_2", 2, ["txn_5", "txn_6"]))
print(N.blockchain_tree)
# N.print_blockchain() # Function not working have to debug


# self.semaphore = threading.Semaphore(0)
# self.queue = Queue() # Queue of events put by the peers or the node itself
# self.event_buffer = collections.defaultdict(set) # Event buffer - which receives events received and forwards it to its peers

# Initialize the blockchain
#  self.blockchain = BlockChain(gen_block, self.pid)
# self.block_timer = None
# # the random no denotes the computation power of the peer. lower the random no, higher the comp. power.
# self.block_gen_mean = Parameters.block_gen_mean * (random.uniform(0.5, 1.0))
