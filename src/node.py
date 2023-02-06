import collections
import random
from queue import Queue

import matplotlib.pyplot as plt
import networkx as nx
from treelib import Tree

from block import *
# from event import *
from parameters import *


class Node:
    def __init__(self, pid, attrb, BTC, num_nodes):

        self.pid = pid  # Unique Id of the peer
        self.cpu = attrb['cpu']  # CPU speed of the peer
        self.hashing_power = attrb['hashing_power']  # Hashing power of the peer
        self.speed = attrb['speed']  # Speed of the peer
        self.peers = {}  # Storing the pointer for function to put events in Queues of peers
        self.BTC = BTC  # Initial BTC balance of the peer
        self.blockchain_tree = {"Block_0": {"parent": None}} # Blockchain tree of the peer
        self.blockchain = {"Block_0":Block(None,None,None,None,0,[100]*num_nodes,0,0)}  # Blockchain of the peer - stores the block objects, Initially the genesis block is added
        self.longest_chain = ["Block_0"] # Longest chain of the peer as a list of block ids
        self.max_len = 0  # Length of the longest chain
        self.txn_list = []  # List of transactions that the peer has seen but not included in any block
        self.included_txn = []  # List of transactions that the peer has included in a block
        self.block_buffer = []  # List of blocks that the peer has heard but not added to its blockchain because parent block is not yet added
        self.blocksReceiveTime = []
    # receives the pointer of the neighbor's enqueue function from the Network class and puts it in his list -
    # so that it can communicate anything by putting events in the neighbour's queue
    def add_peer_pointer(self, pid, receive_event_function):
        self.peers[pid] = receive_event_function

    # Debugging the function pointer list
    def print_funct_points(self):
        print(self.peers)

######################################################################################################################################################
    # The following functions will be used to add the block that the node has heard, to its blockchain and remove common TXNs from its TXN pool
     
    # Function to add a block to the blockchain
    def add_block(self, block):
        for i in range(len(self.block_buffer)):
            self.add_block(self.block_buffer[i])
        if block.previous_id in self.blockchain.keys(): # Checking if the parent block is already in the blockchain
            self.add_block_to_chain(block)
        elif block.previous_id not in self.block_buffer:
            self.block_buffer.append(block) # Adding the block to the block buffer
        

    def add_block_to_chain(self, block):
        if self.validate_block(block): # Checking if the block is valid
            self.blockchain[block.block_id] = block # Adding the block to the blockchain
            self.blockchain_tree[block.block_id] = {"parent": block.previous_id} # Adding the block to the blockchain tree
            # self.blockchain_tree[block.block_id] = {"parent": self.longest_chain[-1]}
            # self.blockchain[block.block_id].length = self.blockchain[self.longest_chain[-1]].length + 1
            self.blockchain[block.block_id].length = self.blockchain[block.previous_id].length + 1 # Updating the length of the block
            self.included_txn.extend(block.transactions) # Adding the transactions to the list of included transactions
            self.remove_common_TXN(block) # Removing the transactions from the list of transactions that the peer has seen but not included in any block
            if self.blockchain[block.block_id].length >= self.max_len: # Checking if the block is the longest block
                self.max_len = self.blockchain[block.block_id].length # Updating the length of the longest chain
                self.longest_chain = self.find_longest_chain() # Updating the longest chain
            print(f"{self.pid} says {block.block_id} is valid and added to its blockchain")
            return True
        else:
            print(f"{self.pid} says {block.block_id} is invalid")
            return False
    
    def remove_common_TXN(self, block): # Removing the transactions that are included in the block from the list of transactions that the peer has seen but not included in any block
        for txn in block.transactions:
            if txn in self.txn_list:
                self.txn_list.remove(txn)

    def find_parent_txns(self,block):
        txns = []
        parent = block.previous_id
        while parent != "Block_0":
            if parent in self.blockchain.keys():
                txns.extend(self.blockchain[parent].transactions)
                parent = self.blockchain_tree[parent]["parent"]
        return txns

    # Function to find the longest chain in the blockchain
    def find_longest_chain(self):
        longest_chain = []
        max_block_id = "Block_0"
        max_length = 0
        for block_id,block in self.blockchain.items():
            if block.length > max_length: # Finding the block with the maximum length
                max_block_id = block_id
            elif block.length == max_length:
                if int(block.block_id[6:]) < int(self.blockchain[max_block_id].block_id[6:]):
                    max_block_id = block.block_id
        while max_block_id != None: # Traversing backwards till the genesis block
            longest_chain.append(max_block_id)
            max_block_id = self.blockchain_tree[max_block_id]["parent"]
        return longest_chain[::-1]

    # Function to check if the block is valid
    # Assuming a global transaction list and a global balance list
    # SIMULATOR MAY GENERATE BLOCKS WITH SAME TXNs, BUT RECEIVING NODE WILL NOT VALIDATE
    def validate_block(self, block):
        # return True
        if block.previous_id not in self.blockchain: # Checking if the previous block is in the blockchain
            return False
        parent_txns = self.find_parent_txns(block)
        for txn in block.transactions:
            if txn in parent_txns: # Checking if the transaction is already included in the blockchain
                print(self.pid,"says that",txn,"is already there in the chain")
                return False
            else:
                return True # Assuming that a block is broadcasted only if the balances are non-negative and hence the block is valid

########################################################################################################################################
    # The following function will be used at the time of creating and forwarding TXNs

    def add_txn(self, txn_id): # Adding a transaction to the list of transactions that the peer has seen but not included in any block
        if txn_id not in self.txn_list:
            self.txn_list.append(txn_id)
        else:
            print(f"{self.pid} says {txn_id} is already in the list of transactions")

########################################################################################################################################
    # The following function will be used when node is trying to create new block

    # Get TXN from the TXN pool which are not yet included in any block that the node has heard
    def get_TXN_to_include(self):
        print("TXN POOL:",self.txn_list)
        if len(self.txn_list) > 999:
            upper_limit = 999
        else:
            upper_limit = len(self.txn_list)
        num_txn_to_mine = random.randint(0,upper_limit) # Number of transactions to be included in the block
        txn_to_mine = random.sample(self.txn_list,num_txn_to_mine) # Transactions to be included in the block
        print("TXN to include: ",num_txn_to_mine)
        return txn_to_mine

    def get_PoW_delay(self):
        return random.expovariate(self.hashing_power/I) # Mining time of the block

#########################################################################################################################################
    # Following function will be used at the end to print the blockchain (tree form) of the node
    def print_blockchain(self):
        dict_ = self.blockchain_tree.copy()
        # added = set()
        # tree = Tree()
        # while dict_:  # while dict_ is not empty
        #     for key, value in dict_.items():
        #         if value['parent'] in added:
        #             tree.create_node(key, key, parent=value['parent'])
        #             added.add(key)
        #             dict_.pop(key)
        #             break
        #         elif value['parent'] is None:
        #             tree.create_node(key, key)
        #             added.add(key)
        #             dict_.pop(key)
        #             break
        # tree.show()
        G = nx.Graph()
        for key, value in dict_.items():
            if value['parent'] is not None:
                G.add_node(key)
                G.add_edge(key, value['parent'])
            else:
                G.add_node(key)

        plt.figure(figsize=(10, 10))
        nx.draw(G, with_labels=True)
        plt.show()
#############################################################################################################################################
    # The following function is to validate the TXNs in the block 
    def validate_TXNs(self, simulator, block):
        for txn_id in block.transactions[:-1]:
            txn = simulator.global_transactions[txn_id]
            if block.balances[txn.sender_id]<0:
                return False
        return True

    def update_balances(self,simulator,block):
        for txn_id in block.transactions[:-1]:
            txn = simulator.global_transactions[txn_id]
            block.balances[txn.sender_id]-=txn.amount
            block.balances[txn.receiver_id]+=txn.amount
        # block.balances[block.transactions[-1].receiver_id]+=block.transactions[-1].amount
        return block 

# Testing the code
if __name__ == "__main__":
    N = Node(1, {"cpu": "low", "speed": "high","hashing_power" : 0.1}, 100,100)
    N.add_block(Block(1, "Block_0", 0,[100,100], ["txn_1", "txn_2"],2))
    N.add_block(Block(2, "Block_0", 1, [100,100],["txn_3", "txn_4"],2))
    N.add_block(Block(3, "Block_1", 2,[100,100], ["txn_5", "txn_6"],2))
    print(N.blockchain_tree)
    print(N.find_longest_chain())
    print(f"Maximum length: {N.max_len}")
    print(N.included_txn)
    N.add_txn(N.included_txn[2]) 
    print(N.txn_list)
    N.add_txn("txn_3")


