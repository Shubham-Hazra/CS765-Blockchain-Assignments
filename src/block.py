# Class for block

class Block:
    def __init__(self, block_id, creator_id, previous_block_id, transactions, length, prev_block_len): # length - stores the length of the block from the genesis block in the 
        self.id  =  block_id # Set the ID of the block
        self.creator_id = creator_id
        self.previous_id = previous_block_id
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
    b1 = Block(0, 0, 1, 1, 1, 1)
    b1.print_block()
