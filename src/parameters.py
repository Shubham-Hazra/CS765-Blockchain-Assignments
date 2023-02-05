num_peers = 50    # total number of peers
z0 = 10         # Slow node percentage
z1 = 10          # Low CPU node percentage
start_balance = 100

# Transaction parameters
txn_gen_mean = 5  # transaction generation time mean
txn_per_block = 10

# Block parameters
block_gen_mean = 125  # Tk mean
block_generation_fee = 50

# Temporary
num_neighbours = 4

# Latency parameters
p_min = 0.01
p_max = 0.50
m = 8.0 * (10**6)
c_high = 100.0 * (10**6)
c_low = 5.0 * (10**6)
d = 96.0 * (10**3)

# Peer parameters
a = {}
MAX = "END"
a["P_0"] = '\033[95m'
a["P_1"] = '\033[94m'
a["P_2"] = '\033[93m'
a["P_3"] = '\033[92m'
a["P_4"] = '\033[91m'
a["END"] = '\033[0m'
for i in range(5, num_peers):
    a["P_"+str(i)] = a["P_"+str(i % 5)]

CURRENT_TIME = 0 # Current time of the simulation
I = 6 # Average inter arrival time between two consecutive blocks