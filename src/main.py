import argparse

from simulate import Simulator

# Take command line arguments
cli = argparse.ArgumentParser() # Command line interface
cli.add_argument("--n", type=int, default=100, help="Number of nodes")
cli.add_argument("--z0", type=int, default=10, help="Percentage of slow nodes")
cli.add_argument("--z1", type=int, default=10, help="Percentage of low CPU nodes")
cli.add_argument("--Ttx", type=int, default=3, help="Mean transaction interarrival time")
cli.add_argument("--I", type=int, default=10, help="Mean block interarrival time")
cli.add_argument("--steps", type=int, default=10, help="The number of steps to run the simulation for")

args = cli.parse_args()

if __name__ == "__main__":
    print(args.n)
    print(args.z0)
    print(args.z1)
    print(args.Ttx)
    print(args.I)
    print(args.steps)
    simulator = Simulator(args.n, args.z0, args.z1, args.Ttx, args.I, args.steps)
    simulator.run() # Run the simulation
