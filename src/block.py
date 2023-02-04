# Class for block
class Block:
    def __init__(self, block_id, creator_id, previous_block_id,create_time, prev_block_len,transactions): # length - stores the length of the block from the genesis block in the 
        self.id  =  block_id # Set the ID of the block
        self.creator_id = creator_id # Set the ID of the creator of the block
        self.previous_id = previous_block_id # Set the ID of the previous block
        self.create_time = create_time # Set the time of creation of the block
        self.length = prev_block_len + 1  # Increment block length
        self.transactions = transactions # List of all the TXNs

    # Function for printing block information
    def print_block(self):
        print("Block id: ", self.id)
        print("Block creator id: ", self.creator_id)
        print("Block previous: ", self.previous_id)
        print("Block position from Genesis block: ", self.length)
        print("Block transactions: ", self.transactions)

# Testing
if __name__ == '__main__':
    b1 = Block(0, 0, 1,0, 1, ["Txn_1", "Txn_2"])
    b1.print_block()
