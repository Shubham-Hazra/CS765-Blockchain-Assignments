import argparse
import os

from simulate import Simulator

# Take command line arguments
cli = argparse.ArgumentParser() # Command line interface
cli.add_argument("--n", type=int, default=100, help="Number of nodes") # Number of nodes
cli.add_argument("--z0", type=int, default=10, help="Percentage of slow nodes") # Percentage of slow nodes
cli.add_argument("--z1", type=int, default=10, help="Percentage of low CPU nodes") # Percentage of low CPU nodes
cli.add_argument("--Ttx", type=int, default=3, help="Mean transaction interarrival time") # Mean transaction interarrival time
cli.add_argument("--I", type=int, default=10, help="Mean block interarrival time") # Mean block interarrival time
cli.add_argument("--steps", type=int, default=10, help="The number of steps to run the simulation for") # The number of steps to run the simulation for

args = cli.parse_args() # Parse the arguments

if __name__ == "__main__":
    simulator = Simulator(args.n, args.z0, args.z1, args.Ttx, args.I, args.steps)
    folders = os.listdir()
    if 'blockchain_tree' not in folders:
        os.mkdir('blockchain_tree')
    if 'networkx_graph' not in folders:
        os.mkdir('networkx_graph')
    for node in simulator.N.nodes:
        node.dump_blockchain_tree()
        node.dump_networkx_graph()
        
