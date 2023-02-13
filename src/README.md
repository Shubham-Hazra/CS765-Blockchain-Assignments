# Description
This aim of this assignment is to build a discrete-event simulator for a P2P cryptocurrency network
- `block.py`        - Block structure
  - Contains block id, creator id, id of previous block, creation time, transactions,length from genesis block, balances of each peer and some other miscellaneous fields for implementation purposes 

- `transaction.py`  - Transaction structure
  - Contains txn id, sender id, receiver id, amount
  - Also contains a message of the form :
    - TxnID: $\textrm{ID}_x$ pays $\textrm{ID}_y$ C coins, if it is a normal transaction
    - TxnID: $\textrm{ID}_k$ mines C coins, if it is a coinbase transaction
  - Contains some other miscellaneous fields for implementation purposes

- `network.py` - Network structure

- `node.py`   - Node structure for each peer
  - Owned by each peer
  - Contains tree structure of blockchain
  - Manages adding new Transactions and new Blocks to Blockchain

- `peer.py`         - Peer structure
  - Contains async gen_transaction and gen_block
  - Contains thread safe Queue for reveiving messages
  - Note that we have used Semaphores to manage and process Queues in an async fashion
  - process_message manages sending message in a loopless fashion
  - render manages rendering the blockchain for the current peer

- `event.py`         - Peer structure

- `simulate.py`    - Simulates Peers' interaction
  - Generates and simulates the blockchain network
  - Simulator spawns individual independent peer threads
  - Peer threads' interaction is managed and documented

- `main.py`         - Main function

# How to run
In the source directory run `python3 main.py --n [n] --z0 [z0] --z1 [z1] --Ttx [Ttx] --I [I] --steps [steps]` \
For eg: `python main.py --n 100 --z0 10 --z1 40 --Ttx 10 --I 60 --steps 100000` \
By default, simulations run for a maximum of 100000 steps \
Use number of nodes to be $\geq 15$ to be safe \