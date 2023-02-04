# Class for block
class Block:
    _id = 0 # Global block ID
    def __init__(self,creator_id, previous_block_id,create_time, transactions,block_id = None,length = 0): # length - stores the length of the block from the genesis block in the 
        Block._id += 1 # Increment the global block ID
        block_id = Block._id 
        self.id  =  f"Block_{block_id}" # Set the ID of the block
        self.creator_id = creator_id # Set the ID of the creator of the block
        self.previous_id = previous_block_id # Set the ID of the previous block
        self.create_time = create_time # Set the time of creation of the block
        self.transactions = transactions # List of all the TXNs
        self.length = length # Length of the block initially set to 0


    def get_size(self): # Function to get the size of the block
        return 1 + len(self.transactions)

    # Function for printing block information
    def print_block(self):
        print("Block id: ", self.id)
        print("Block creator id: ", self.creator_id)
        print("Block previous: ", self.previous_id)
        print("Block transactions: ", self.transactions)

# Testing
if __name__ == '__main__':
    b1 = Block(0, 1, 1, ["Txn_1", "Txn_2"])
    b1.print_block()
    b2 = Block(1, 2, 2, ["Txn_3", "Txn_4"])
    b2.print_block()
