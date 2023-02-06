import random
import time

from block import Block
from network import Network
from transaction import Transaction


class Event(object):

    def __init__(self, node_id, creator_id, create_time, run_time):
        super(Event, self).__init__()
        self.node_id = node_id
        self.creator_id = creator_id
        self.create_time = create_time
        self.run_time = run_time 

    def __lt__(self, non_self):
        # To define a < operator to put into the Priority Queue
        return self.run_time < non_self.run_time

    # Function for printing message information
    def print(self):
        print("Event from " + str(self.creator_id) + " at time " +
              str(self.run_time) + " running on node", str(self.node_id))

class CreateTXN(Event):
    def __init__(self, node_id, creator_id, create_time, run_time): # N is the network for extracting peer information
        super(CreateTXN, self).__init__( # Inherits the Event class - whenever CreateTXN object is created, Event (parent) class is initialized
            node_id, creator_id, create_time, run_time
        )     

    def addEvent(self, N, simulator) :  

        # Creates a TXN setting:
        # 1. randomly assigns a receiving node
        # 2. randomly chooses an amount
        # 3. checks whether the balances of sender and receiver are sane after the TXN is created
        # 4. Adds the CreateTXN event after a random time interval
        # 4. adds the ReceiveTXN Event in the Queue for those peers who have not yet received the TXN (ensured through a Boolean array associated with the Event)

        current = N.nodes[self.node_id]

        # 1. Randomly select a receiver
        receiver = list(set(N.nodes) - set([current]))
        receiver = random.choice(receiver)

        # 2. randomly generate TXN amount 
        TXN_amount = 1.2*current.BTC * random.uniform(0, 1) # Some probability that the TXN generated is inavlid

        # 3. Update the balance if TXN is invalid else exit the event
        if self.check_TXN(current, receiver, TXN_amount):
            self.update_balance(current, receiver, TXN_amount)
        else:
            print("Invalid TXN: Payer balance:", current.BTC, " Receiver balance:", receiver.BTC, " TXN amount: ", TXN_amount)
            return

        new_txn = Transaction(simulator.txn_id, self.node_id, receiver.pid,TXN_amount, len(N.nodes))
        simulator.txn_id += 1

        # For debugging
        print("TXN Gen:", self.node_id ,"heard that ", end= " ")
        new_txn.print_transaction()

        # Since this node has itself created the TXN, flip its value to 1 in the boolean array
        new_txn.received[self.node_id] = 1

        # Add the TXN id to the TXN pool of the creator
        current.add_txn(new_txn.id)

        # simulator.events.put(CreateTXN(
        #     self.node_id,
        #     self.node_id,
        #     self.run_time,
        #     self.run_time + simulator.transaction_delay()
        # ))

        # 4. adds the ReceiveTXN Event in the Queue for those peers who have not yet received the TXN (ensured through a Boolean array associated with the Event)
        for neighbor in N.G.neighbors(self.node_id):
            t = N.calc_latency(self.node_id, neighbor, .008) # TXN is 8000 bits = 1KB = .008MB
            new_txn.received[neighbor] = 1
            simulator.events.put(ReceiveTXN(
                new_txn,
                neighbor,
                self.node_id,
                self.run_time,
                self.run_time + t
            ))
        
    def check_TXN(self, sender, receiver, TXN_amount):
        return (sender.BTC - TXN_amount >=0) and (receiver.BTC >=0)

    def update_balance(self, sender, receiver, TXN_amount):
        sender.BTC -= TXN_amount
        receiver.BTC += TXN_amount

class ReceiveTXN(Event):

    def __init__(self, transaction, node_id, creator_id, create_time, run_time):
        super(ReceiveTXN, self).__init__(
            node_id, creator_id, create_time, run_time
        )
        self.transaction = transaction

    def addEvent(self, N, simulator):
        # Create object of the current node
        current = N.nodes[self.node_id]

        # For debugging
        print("TXN Fwd:", self.node_id, "heard that ", end = " ")
        self.transaction.print_transaction()

        # Add the TXN id to the TXN pool of the creator
        current.add_txn(self.transaction.id)

        # 4. adds the ReceiveTXN Event in the Queue for those peers who have not yet received the TXN (ensured through a Boolean array associated with the Event)
        for neighbor in N.G.neighbors(self.node_id):
            if self.transaction.received[neighbor] == 0:
                t = N.calc_latency(self.node_id, neighbor, .008) # TXN is 8000 bits = 1KB = .008MB
                self.transaction.received[neighbor] = 1
                simulator.events.put(ReceiveTXN(
                    self.transaction,
                    neighbor,
                    self.node_id,
                    self.run_time,
                    self.run_time + t
                ))

class ForwardBlock(Event):
    def __init__(self, block, node_id, creator_id, creat_time, run_time):
        super(ForwardBlock, self).__init__(
            node_id, creator_id, creat_time, run_time
        )
        self.block = block
    
    def addEvent(self, N, simulator): 
        current = N.nodes[self.node_id]

        # Do nothing if the block has already been seen
        if not self.block.block_id in current.blockchain.keys(): 
            # Return the ID of the previous block
            prev_blk_id = current.blockchain.get(self.block.previous_id)
            if prev_blk_id is None:
                print("BLOCK ERROR on",self.node_id,": Previous Block has not arrived")
            else: # If previous block has arrived
                # # Make a new block to add to the node's tree
                new_block = Block(
                    self.block.creator_id,
                    prev_blk_id.block_id,
                    self.block.created_at,
                    self.block.transactions,
                    N.num_nodes,
                    self.block.block_id[6:]
                )
                print("previous ID of the block is",new_block.previous_id)
                # Add the block to the blockchain of the node and removes common TXNs from the TXN pool of the node
                current.add_block(new_block)
        else:
            print("ONLY FORWARDING BLOCK on",self.node_id,":",self.node_id,"has already added",self.block.block_id,"into his blockchain")

        # To store the arrival time of the block received, between t_k and t_k + T_k, during PoW, to ensure that no other block had come between t_k and t_k + T_k - so that the node can create a block
        current.blocksReceiveTime.append(self.block.created_at) # To store the execution time of the event so that we can ensure no block has arrived between t_k and T_k

        # Forwarding the block to its peers
        for neighbor in N.G.neighbors(self.node_id):

            # Exclude the crator of the block
            if neighbor != self.block.creator_id and self.block.received[neighbor] == 0:

                t = N.calc_latency(self.node_id, neighbor, self.block.get_size()) # To calculate the latency of the block based on the number of transactions in the block
                self.block.received[neighbor] = 1 # That the node has seen the block
                simulator.events.put(ForwardBlock(
                    self.block,
                    neighbor,
                    self.node_id,
                    self.run_time,
                    self.run_time + t
                ))
        #######################################################################################################################################
        # After the block receives the Block from its peers, The node starts the PoW again - See last paragraph of the Problem statement 7th statement
        #######################################################################################################################################
        print("STARTING POW on",self.node_id)
        PoW_delay = current.get_PoW_delay()
        print("PoW delay for", self.node_id,"is",PoW_delay)
        simulator.events.put(MineBlock( ################ THIS CORRESPONDS TO TIME t_k - the TIME FROM WHICH THE NODE WAITS TO CHECK WHETHER ANY OTHER BLCK RRIVES OR NOT (for T_k time)
            self.node_id,
            self.node_id,
            self.run_time,
            self.run_time + PoW_delay # Updated block_delay() as described in simulating PoW section
        ))
        

class MineBlock(Event):
    def __init__(self, node_id, creator_id, create_time, run_time):
        super(MineBlock, self).__init__(
            node_id, creator_id, create_time, run_time)
        
    def addEvent(self, N, simulator):
        current = N.nodes[self.node_id]

        # for x in current.blocksReceiveTime:
        #     if x > self.run_time:
        #         return
        # The block generation event was created at t_k (create_time) and scheduled for t_k + T_k (run_time) 
        # if there is some block in the list of blocks seen by the node such that it reached that node at timet,t_k < t < t_k + T_k then reject this block generation event
        for block_rcv_time in current.blocksReceiveTime: 
            if block_rcv_time > self.create_time and block_rcv_time < self.run_time:
                print("MINING UNSUCCESSFUL: PoW on",self.node_id,"Unsuccessful :(, some other node has created the block")
                return

        # Traverse the longest chain and find all transactions that've been spent
        last_blck = current.longest_chain[-1]# Stores the id of the block which is being mined in the blockchain of that node

        # print("LONGEST CHAIN FOUND")
        # print(longest_chain)

        # Get TXn to be included in the block (all the maximum limits and other conditions are handled by the node)
        # To terminate the block mining process if the node has no TXNs to include in the block
        if not current.txn_list:
            print("MINING UNSUCCESSFUL: No TXN to include")
            return 

        txn_to_include = current.get_TXN_to_include()

        # print("TRANSACTIONS TO INCLUDE")
        # print(txn_to_include)

        # To terminate the block mining process if the node has no TXNs to include in the block        
        if not txn_to_include:
            print("MINING UNSUCCESSFUL: No TXN to include")
            return
        
        # Include the mining fee TXN in the block
        miningTXN = Transaction(simulator.mining_txn_id, current.pid, current.pid, 50, N.num_nodes)
        txn_to_include.append(miningTXN.id)

        # print("APPENDING MINING FEE TXN")
        # print(txn_to_include)
    
        # Generate a new block
        new_blk = Block(current.pid,last_blck, self.run_time, txn_to_include,N.num_nodes, simulator.block_id, len(current.longest_chain))
        print("BLOCK ID:",new_blk.block_id,", PREVIOUS POINTER:",new_blk.previous_id)
        simulator.block_id += 1
        simulator.mining_txn_id-=1

        print("MINING SUCCESSFUL: NEW BLOCK GENERATED")
        new_blk.print_block()

        # Add the block to my chain
        current.add_block(new_blk)

        # Update the mining reward in the creator's block
        current.BTC += 50

        # Forwarding the block to its peers
        for neighbor in N.G.neighbors(self.node_id):

            # Exclude the crator of the block
            if neighbor != new_blk.creator_id:

                t = N.calc_latency(self.node_id, neighbor, new_blk.get_size()) # To calculate the latency of the block based on the number of transactions in the block
                new_blk.received[neighbor] = 1 # That the node has seen the block
                simulator.events.put(ForwardBlock(
                    new_blk,
                    neighbor,
                    self.node_id,
                    self.run_time,
                    self.run_time + t
                ))
                









    

    











# # Function for sending message
# def send(self, receiver_function, sleep_time):
#     def send_message():
#         time.sleep(sleep_time)  # Sleep for sleep_time seconds
#         receiver_function(self)
#     # Create thread i.e. Call send_message function
#     t = threading.Thread(target=send_message)
#     t.start()
