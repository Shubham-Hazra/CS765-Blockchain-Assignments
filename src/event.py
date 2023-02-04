from transaction import Transaction
from network import Network
import random
import time

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

        # simulator.events.put(CreateTXN(
        #     self.node_id,
        #     self.node_id,
        #     self.run_time,
        #     self.run_time + simulator.transaction_delay()
        # ))

        # 4. adds the ReceiveTXN Event in the Queue for those peers who have not yet received the TXN (ensured through a Boolean array associated with the Event)
        for neighbor in N.G.neighbors(self.node_id):
            t = N.calc_latency(self.node_id, neighbor, 8000) # TXN is 8000 bits

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

    def __init__(self, transaction, node_id, creator_id, created_at, run_at):
        super(ReceiveTXN, self).__init__(
            node_id, creator_id, created_at, run_at
        )
        self.transaction = transaction

    def addEvent(self, N, simulator):
        # Check the boolean array whether the node has already seen this txn
        if self.transaction.received[self.node_id] == 1: # Already seen this TXN
            print(self.node_id, "has already seen this TXN")
            return
        else:
            self.transaction.received[self.node_id] = 1

        # For debugging
        print("TXN Fwd:", self.node_id, "heard that ", end = " ")
        self.transaction.print_transaction()

        # 4. adds the ReceiveTXN Event in the Queue for those peers who have not yet received the TXN (ensured through a Boolean array associated with the Event)
        for neighbor in N.G.neighbors(self.node_id):
            t = N.calc_latency(self.node_id, neighbor, 8000) # TXN is 8000 bits

            simulator.events.put(ReceiveTXN(
                self.transaction,
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
