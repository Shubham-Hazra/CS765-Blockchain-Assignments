import pickle
import random

import matplotlib.pyplot as plt
import networkx as nx
from treelib import Tree

f = open('networkx_graph/0.pkl', 'rb')
networkx_graph = pickle.load(f)
plt.figure(figsize=(10, 10))
nx.draw(networkx_graph, with_labels=True)
plt.show()
f.close()

f = open('blockchain_tree_dict/0.pkl', 'rb')
blockchain_tree_dict = pickle.load(f)
print(blockchain_tree_dict)
f.close()

tree = Tree()
tree.create_node("Block_0", "Block_0")
for block in blockchain_tree_dict.keys():
    if block == "Block_0":
        continue
    tree.create_node(block,block, parent = blockchain_tree_dict[block]['parent'])
tree.show()
