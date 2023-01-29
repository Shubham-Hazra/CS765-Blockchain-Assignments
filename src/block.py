import threading


# Class for block header
class Block_header:
    def __init__(self, version=1, prev_block_hash=None, merkle_root_hash=None, timestamp=None, target=None, nonce=None):
        self.version = version
        self.prev_block_hash = prev_block_hash
        self.merkle_root_hash = merkle_root_hash
        self.timestamp = timestamp
        self.target = target
        self.nonce = nonce

# Class for block


class Block:
    id = 0  # Global block id
    lock = threading.Lock()  # Lock for block id

    def __init__(self, previous_block_id, previous_block_len, balances, transactions, all_transactions, creator_id, block_header=Block_header()):
        Block.lock.acquire()  # Lock block id
        Block.id += 1  # Increment global block id
        self.id = f"Block_{Block.id}"  # Set block id
        self.creator_id = creator_id
        Block.lock.release()  # Unlock block id
        self.block_header = block_header
        self.previous_id = previous_block_id
        self.length = previous_block_len + 1  # Increment block length
        self.balances = balances
        self.transactions = transactions
        self.all_transactions = all_transactions

    # Function for printing block header information
    def print_block_header(self):
        print("Block header version: ", self.block_header.version)
        print("Block header previous block hash: ",
              self.block_header.prev_block_hash)
        print("Block header merkle root hash: ",
              self.block_header.merkle_root_hash)
        print("Block header timestamp: ", self.block_header.timestamp)
        print("Block header target: ", self.block_header.target)
        print("Block header nonce: ", self.block_header.nonce)

    # Function for printing block information
    def print_block(self):
        print("Block id: ", self.id)
        print("Block length: ", self.length)
        print("Block previous: ", self.previous_id)
        print("Block balances: ", self.balances)
        print("Block transactions: ", self.transactions)
        print("Block all transactions: ", self.all_transactions)
        print("Block creator id: ", self.creator_id)


# Testing
if __name__ == '__main__':
    b1 = Block(0, 0, 1, 1, 1, 1)
    b2 = Block(1, 1, 2, 2, 2, 2, Block_header(2, 2, 2, 2, 2, 2))
    b1.print_block()
    print()
    b2.print_block()
    print()
    print(f"Version: {b1.block_header.version}")
    b2.print_block_header()
