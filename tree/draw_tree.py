from tree.syntax_tree import Node

def print_tree(node : Node, level=0):
    if node is not None:
        if node.is_star():
            print_tree(node.child, level + 1)
            print(' ' * 6 * level + '->', str(node))
        else :
            print_tree(node.right, level + 1)
            print(' ' * 6 * level + '->', str(node))
            print_tree(node.left, level + 1)

# Use it like this:
# print_tree(root)

