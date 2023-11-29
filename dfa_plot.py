import networkx as nx
import matplotlib.pyplot as plt
import numpy.random as nprand

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
    
    rad = nprand.randint(1, 50) / 100 # 29 / 100 = 0.29
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color='b', arrows=True, connectionstyle=f"arc3, rad={rad}")

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
