import random


def get_PoW_delay(hashing_power, I):
    return random.expovariate(hashing_power/I) # Mining time of the block

def transaction_delay(Ttx):
    return random.expovariate(1 /Ttx)

def calc_latency(c,packet_size):# Returns the latency between two nodes (packet_size is the size of the message in Mbs)
    l = random.uniform(10, 500)/1000
    d = random.expovariate((c*1000)/96)
    print(f"l: {l}, d: {d}")
    return l+ packet_size/c + d

if __name__ == '__main__':
    l = []
    for i in range(100):
        l.append(get_PoW_delay(1, 600))
    mean = sum(l)/len(l)
    print(f"Mean block: {mean}")

    l = []
    for i in range(100):
        l.append(transaction_delay(0.01))
    mean = sum(l)/len(l)
    print(f"Mean transaction: {mean}")

    print(f"Latency: {calc_latency(5,.001)}")
