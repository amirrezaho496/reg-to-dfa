import tree.syntax_tree as stree
import tree.d_tran as dtran
import tree.draw_tree as draw_tree
import dfa_plot as dplt

print("____________________________")
print("Developers : \n")
for Developer in stree.DEVELOPERS :
    print(Developer)
print("____________________________", "\n")
root = stree.Node()
root = root.read_tree_preorder()
TREE_ROOT = root

print("____________________________")
print("tree plot :")
draw_tree.print_tree(root)
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
for n in range(1,stree.NODES_NUMBERS):
    if fp_table[n] == set():
        char = '%'
    else:
        char = fp_table[n]
    print(f"{n} : {char}")

print("____________________________")
print("Alphabet table :\n")
alpha_dict = stree.get_alphabet_dict()
print(alpha_dict)


print("____________________________")
print("D Tran table :\n")
d_tran = dtran.DTran(fp_table=fp_table, alpha_dict=alpha_dict)

# set firstpos of root as start state
d_tran.create_d_tran(root.firstpos)

d_tran.print_d_tran()
# print("____________________________")
# print('Table : \n')

# d_tran.print_d_tran_table()

dfa = d_tran.convert_dtran_to_dict()
start_state = d_tran.get_item_by_state(root.firstpos)
final = d_tran.get_final_states_ids()
dplt.draw_dfa(dfa, start_state.id, final)