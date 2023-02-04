from treelib import Node, Tree

dict_ = {"2": {'parent': "1"}, "1": {'parent': None},
         "3": {'parent': "2"}, "4": {'parent': "2"}}

added = set()
tree = Tree()
while dict_:

    for key, value in dict_.items():
        if value['parent'] in added:
            tree.create_node(key, key, parent=value['parent'])
            added.add(key)
            dict_.pop(key)
            break
        elif value['parent'] is None:
            tree.create_node(key, key)
            added.add(key)
            dict_.pop(key)
            break

tree.show()
