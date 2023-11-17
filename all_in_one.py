
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

# dfa_plot.py -------------------------------------------------------------------------------------


def draw_dfa(dfa, start_state: str, final_states:list):
    G = nx.MultiDiGraph()
    for state in dfa:
        for letter, destination in dfa[state].items():
            G.add_edge(state, destination, label=letter)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))

    # green is for start state, blue for normal states, red for final sta 
    # M for nodes what are start and final
    node_colors = []
    for node in G.nodes():
        if node == start_state:
            if node in final_states:
                node_colors.append('m')
            else:
                node_colors.append('g')
        elif node in final_states:
            node_colors.append('r')
        else:
            node_colors.append('b')
    pass

    nx.draw_networkx_nodes(G, pos, cmap= plt.get_cmap('jet'), 
                           node_color = node_colors)
    
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color='b', arrows=True, connectionstyle='arc3, rad=0.1')

    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
            
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()

# Example usage:
# dfa = {
#     'A': {'0': 'A', '1': 'B'},
#     'B': {'0': 'A', '1': 'C'},
#     'C': {'0': 'C', '1': 'C'},
# }
# start_state = 'A'
# final_states = ['C']
# draw_dfa(dfa, start_state, final_states)



# syntax_tree.py -------------------------------------------------------------------------------------

STAR = "*"
OR = "|"
CONCAT = "."
EPSILON = "E"
SHARP = "#"

OPERATORS = [STAR, OR, CONCAT]
NODES_NUMBERS = 1
ALHPA_DICT: dict[int, str] = {}
TREE_ROOT  = None

DEVELOPERS = ["AMIRREZA HOSSEINI DEHLAGHI", "ALI HOJATI", "ALI EBRAHIMI", "MOHAMMAD REZA SAEEDIAN JAZI"]

class Node:
    def __init__(self, data=None):
        self.data: str = data
        self.nullable: bool = True
        self.left: Node = None
        self.right: Node = None
        self.firstpos = set()
        self.lastpos = set()
        self.followpos = set()
        self.child: Node = None
        self.number: int = None
        
    def __str__(self) -> str:
        if self.is_operator():
            return f"{self.data}"
        
        return f"{self.data}:{self.number}" 

    def is_star(self) -> bool:
        return self.left is None and self.right is None and self.child is not None

    def is_operator(self):
        return OPERATORS.__contains__(self.data)

    def read_tree_preorder(self):
        """
        Create a new node for root of the tree
        get syntax-tree data from user input
        and number them (start from 1) \n
        Returns:
            Node: root of the tree \n
            dict[int, str] : a dictionary of the leaf.data and leaf.number
        """
        data = input("Enter node data (or '@' to finish): ")

        if data.lower() == "@":
            return None

        self.data = data
        # check if its operator or not
        if self.is_operator():
            # STAR has one child
            if data == STAR:
                print("Enter child of " + data)
                self.child= Node().read_tree_preorder()
            else:
                print("Enter left child of " + data)
                self.left= Node().read_tree_preorder()

                print("Enter right child of " + data)
                self.right= Node().read_tree_preorder()
        # check if its not Epsilon set a number for it
        elif data != EPSILON:
            set_node_number(self, data)
            #alpha_dict[self.number] = self.data
            pass
        
        return self
    
    def find_nullable(self):
        preorder(self, is_nullable_node)
        pass

    def first_pos(self):
        preorder(self, fisrt_pos_node)
        pass

    def last_pos(self):
        preorder(self, last_pos_node)
        pass

    def follow_pos(self) -> dict[int, set]:
        """
        Calculate nodes follow pos then
        create a dictionary that map number of nodes and their followpos set \n
        Returns:
            dict[int, set] : map node.number -> node.followpos
        """
        fp_finder = FollowPosFinder()

        for number in range(1, NODES_NUMBERS + 1):
            fp_finder.set_number(number)
            fp_finder.make_follow_pos_dict(self)
            pass

        return fp_finder.fp_table

    def complete_tree(self):
        self.find_nullable()


# END of Class Node -----------------------------------------------------------------------


class FollowPosFinder:
    def __init__(self) -> None:
        self.fp_table: dict[int, set] = {}
        self.number: int = None

    def __follow_pos_node(self, node: Node, number: int):
        if node.data == CONCAT:
            # If left child last pos has number
            # add right child first pos
            if node.left.lastpos.__contains__(number):
                self.fp_table[number] = self.fp_table[number].union(node.right.firstpos)
        elif node.data == STAR:
            # If child last pos has number
            # add child first pos
            if node.child.lastpos.__contains__(number):
                self.fp_table[number] = self.fp_table[number].union(node.child.firstpos)

    def make_follow_pos_dict(self, root: Node):
        if root is not None:
            if (root.data == STAR):
                self.make_follow_pos_dict(root.child)
            else:           
                self.make_follow_pos_dict(root.left)
                self.make_follow_pos_dict(root.right)
            
            self.__follow_pos_node(root, self.number)

    def get_fp_table(self):
        return self.fp_table
    
    def set_number(self,n : int):
        if n >= 1:
            self.number = n
            self.fp_table[n] = set()


# END of Class FollowPosFinder ------------------------------------------------------------


def is_nullable_node(node: Node) -> bool:
    if node.data == EPSILON or node.data == STAR:
        node.nullable = True
    elif node.data == CONCAT:
        node.nullable = node.right.nullable and node.left.nullable
    elif node.data == OR:
        node.nullable = node.right.nullable or node.left.nullable
    else:
        node.nullable = False
    
    return node.nullable


def fisrt_pos_node(node: Node):
    if node.data == EPSILON:
        return set()
    elif node.data == STAR:
        node.firstpos = node.child.firstpos
    elif node.data == CONCAT:
        if node.left.nullable:
            node.firstpos = node.left.firstpos.union(node.right.firstpos)
        else:
            node.firstpos = node.left.firstpos
    elif node.data == OR:
        node.firstpos = node.left.firstpos.union(node.right.firstpos)
    else:
        node.firstpos = {node.number}

    print(f"{node.data}: {node.firstpos}")
    return node.firstpos


def last_pos_node(node: Node):
    if node.data == EPSILON:
        return set()
    elif node.data == STAR:
        node.lastpos = node.child.lastpos
    elif node.data == CONCAT:
        if node.right.nullable:
            node.lastpos = node.right.lastpos.union(node.left.lastpos)
        else:
            node.lastpos = node.right.lastpos
    elif node.data == OR:
        node.lastpos = node.left.lastpos.union(node.right.lastpos)
    else:
        node.lastpos = {node.number}

    print(f"{node.data}: {node.lastpos}")
    return node.lastpos


def preorder(node: Node, func):
    if node is not None:
        if node.is_star():
            preorder(node.child, func)
        else:
            preorder(node.left, func)
            preorder(node.right, func)

        func(node)
    pass


def breadth_first(root, func):
    if root is None:
        return

    queue = deque([root])

    while queue:
        node = queue.popleft()
        func(node)

        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    pass


def set_node_number(node: Node, data):
    global NODES_NUMBERS
    global ALHPA_DICT
    
    node.number = NODES_NUMBERS
    ALHPA_DICT[NODES_NUMBERS] = data
    
    NODES_NUMBERS = NODES_NUMBERS + 1
    return node.number


def reset_nodes_number():
    global NODES_NUMBERS
    global ALHPA_DICT
    ALHPA_DICT = {}
    NODES_NUMBERS = 1
    
def get_alphabet_dict():
    return ALHPA_DICT


# d_tran.py -------------------------------------------------------------------------------------

class DTranItem:
    def __init__(self, id: int) -> None:
        self.id = id
        self.state = set()
        self.destination: dict[str, set] = {}
        self.checked: bool = False
        self.is_final: bool = False
        pass

    def set_destination(self, letter: str, destination: set):
        self.destination[letter] = destination
        pass


class DTran:
    def __init__(self, fp_table: dict[int, set] = {}, alpha_dict: dict[int, str] = {}) -> None:
        self.table: list[DTranItem] = []
        self.followpos_table: dict[int, set] = fp_table
        self.alphabet_dict: dict[int, str] = alpha_dict
        pass

    def add_state(self, state: DTranItem):
        self.table.append(state)
        pass

    def get_item_by_state(self, state: set) -> DTranItem:
        for item in self.table:
            if item.state == state:
                return item
        return None
    
    def get_keys_by_letter(self, letter : str):
        keys = set([key for key, value in self.alphabet_dict.items() if value == letter])
        return keys
    
    def get_all_uniq_letters(self):
        return set(self.alphabet_dict.values())
    
    def are_all_states_checked(self):
        for item in self.table:
            if not item.checked:
                return False
        return True
        
        
    def add_destination(self, state: set, letter: str, destination: set):
        item = self.get_item_by_state(state)
        if item is not None:
            item.set_destination(letter, destination)
        pass
    
    def create_d_tran(self, start_state: set):
        self.table.clear()
        id = 1
        first = DTranItem(id)
        first.state = start_state
        self.add_state(first)
        
        all_letters = self.get_all_uniq_letters()
        
        while not self.are_all_states_checked():
            for item in self.table:
                if not item.checked:
                    for letter in all_letters:
                        keys = self.get_keys_by_letter(letter)
                        destination = set()
                        for key in keys:
                            if key in item.state:
                                destination = destination.union(self.followpos_table[key])
                        if destination:
                            existing_item = self.get_item_by_state(destination)
                            if existing_item is None:
                                id += 1
                                new_item = DTranItem(id)
                                new_item.state = destination
                                self.add_state(new_item)
                            item.set_destination(letter, destination)
                    item.checked = True

        self.detect_final_states()
        pass
    
    def detect_final_states(self):
        final_keys = self.get_keys_by_letter(SHARP)
        for item in self.table:
            if any(key in item.state for key in final_keys):
                item.is_final = True
                
    def get_final_states_ids(self):
        return [item.id for item in self.table if item.is_final]

    def print_d_tran(self):
        print(f"{'State ID':<10} {'State':<20} {'Is final':<10} {'Destinations':<20}")
        for item in self.table:
            destinations = ', '.join([f"{letter} --> {str(destination):<20}" for letter, destination in item.destination.items()])
            print(f"{item.id:<10} {str(item.state):<20} {str(item.is_final):<10} {destinations:<20}")

    def print_d_tran_table(self):
        print(f"{'State ID':<10} {'State':<20} {'Is final':<10}")
        for item in self.table:
            print(f"{item.id:<10} {str(item.state):<20} {str(item.is_final):<10}")
            print(f"{'Letter':<10} {'Destination':<20}")
            for letter, destination in item.destination.items():
                print(f"{letter:<10} {str(destination):<20}")
            print("\n")
            
    def convert_dtran_to_dict(dtran):
        dfa = {}
        for item in dtran.table:
            state_transitions = {}
            for letter, destination in item.destination.items():
                # Assuming each state has only one destination for each letter
                destination_item = dtran.get_item_by_state(destination)
                if destination_item is not None:
                    state_transitions[letter] = destination_item.id
            dfa[item.id] = state_transitions
        return dfa



# draw_tree.py -------------------------------------------------------------------------------------

def print_tree(node : Node, level=0):
    if node is not None:
        if node.is_star():
            print_tree(node.child, level + 1)
            print(' ' * 8 * level + '->', str(node))
        else :
            print_tree(node.right, level + 1)
            print(' ' * 8 * level + '->', str(node))
            print_tree(node.left, level + 1)

# Use it like this:
# print_tree(root)

# main.py -------------------------------------------------------------------------------------


print("____________________________")
print("Developers : \n")
for Developer in DEVELOPERS :
    print(Developer)
print("____________________________", "\n")
root = Node()
root = root.read_tree_preorder()
TREE_ROOT = root

print("____________________________")
print("tree plot :")
print_tree(root)
print("____________________________")


root.find_nullable()
print("nullable checked")

print("finding nodes first positions :")
root.first_pos()
print("nodes first positions detected")

print("finding nodes last positions :")
root.last_pos()
print("nodes last positions detected")


fp_table = root.follow_pos()
print("nodes follow positions detected")
print("____________________________")
print("Follow position table :\n")
for n in range(1,NODES_NUMBERS):
    if fp_table[n] == set():
        char = '%'
    else:
        char = fp_table[n]
    print(f"{n} : {char}")

print("____________________________")
print("Alphabet table :\n")
alpha_dict = get_alphabet_dict()
print(alpha_dict)


print("____________________________")
print("D Tran table :\n")
d_tran = DTran(fp_table=fp_table, alpha_dict=alpha_dict)

# set firstpos of root as start state
d_tran.create_d_tran(root.firstpos)

d_tran.print_d_tran()
# print("____________________________")
# print('Table : \n')

# d_tran.print_d_tran_table()

dfa = d_tran.convert_dtran_to_dict()
start_state = d_tran.get_item_by_state(root.firstpos)
final = d_tran.get_final_states_ids()
draw_dfa(dfa, start_state.id, final)