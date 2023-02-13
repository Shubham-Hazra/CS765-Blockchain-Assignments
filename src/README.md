## network.py
1. Use number of nodes to be $\geq 15$ to be safe.

# Description
This aim of this assignment is to build a discrete-event simulator for a P2P cryptocurrency network
- `block.py`        - Block structure
  - Contains block id, creator id, id of previous block, creation time, transactions,length from genesis block, balances of each peer and some other miscellaneous fields for implementation purposes 

- `transaction.py`  - Transaction structure
  - Contains txn id, sender id, receiver id, amount
  - Also contains a message of the form :
    - TxnID: $\textrm{ID}_x$ pays $\textrm{ID}_y$ C coins, if it is a normal transaction
    - TxnID:ID$_k$ mines C coin, if it is a coinbase transaction
  - Contains some other miscellaneous fields for implementation purposes

- `network.py` - Network structure

- `node.py`   - Node structure for each peer
  - Owned by each peer
  - Contains tree structure of blockchain
  - Manages adding new Transactions and new Blocks to Blockchain

- `main.py`         - Main function

- `peer.py`         - Peer structure
  - Contains async gen_transaction and gen_block
  - Contains thread safe Queue for reveiving messages
  - Note that we have used Semaphores to manage and process Queues in an async fashion
  - process_message manages sending message in a loopless fashion
  - render manages rendering the blockchain for the current peer

- `simulator.py`    - Simulates Peers' interaction
  - Generates and simulates the blockchain network
  - Simulator spawns individual independent peer threads
  - Peer threads' interaction is managed and documented



# How to run
run `python3 main.py`