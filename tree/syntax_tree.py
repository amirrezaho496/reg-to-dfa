from collections import deque

STAR = "*"
OR = "|"
CONCAT = "."
EPSILON = "ε"
EPSILON_INPUT = "ep"
SHARP = "#"
EMPTY = "∅"

OPERATORS = [STAR, OR, CONCAT]
NODES_NUMBERS = 1
ALHPA_DICT: dict[int, str] = {}
TREE_ROOT = None

DEVELOPERS = [
    "AMIRREZA HOSSEINI DEHLAGHI",
    "ALI HOJATI",
    "ALI EBRAHIMI",
    "MOHAMMAD REZA SAEEDIAN JAZI",
]


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

        return f"{self.data}{ (':' + str(self.number)) if self.number != None else ''}"

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
        if data == EPSILON_INPUT:
            data = EPSILON

        if data.lower() == "@":
            return None

        self.data = data
        # check if its operator or not
        if self.is_operator():
            # STAR has one child
            if data == STAR:
                print("Enter child of " + data)
                self.child = Node().read_tree_preorder()
            else:
                print("Enter left child of " + data)
                self.left = Node().read_tree_preorder()

                print("Enter right child of " + data)
                self.right = Node().read_tree_preorder()
        # check if its not Epsilon set a number for it
        elif data != EPSILON:
            set_node_number(self, data)
            # alpha_dict[self.number] = self.data
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
        self.number: int | None = None

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
            if root.data == STAR:
                self.make_follow_pos_dict(root.child)
            else:
                self.make_follow_pos_dict(root.left)
                self.make_follow_pos_dict(root.right)

            self.__follow_pos_node(root, self.number)

    def get_fp_table(self):
        return self.fp_table

    def set_number(self, n: int):
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
