import networkx as nx
import matplotlib.pyplot as plt
from numpy.random import rand
from torch import randint

def draw_dfa(dfa, start_state: str, final_states:list):
    G = nx.MultiDiGraph()
    for state in dfa:
        for letter, destination in dfa[state].items():
            G.add_edge(state, destination, label=letter)

    G = convert_multigraph_to_graph(G)  # Convert MultiDiGraph to DiGraph
    
    pos = nx.circular_layout(G)  # Increase distance between nodes
    plt.figure( num="DFA",figsize=(12, 12))  # Increase figure size

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
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors)  # Draw nodes
    nx.draw_networkx_labels(G, pos)  # Draw node labels
    
    for u, v, d in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)])  # Draw edges
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['label']})  # Draw edge labels

    plt.show()  # Display the graph
    
    
def print_dfa(dfa):
    print(f"{'State ID':<10} {'Destinations':<20}")
    for state_id, state_transitions in dfa.items():
        destinations = ', '.join([f"{letter} --> {destination}" for letter, destination in state_transitions.items()])
        print(f"{state_id:<10} {destinations:<20}")


# Example usage:
# dfa = {
#     'A': {'0': 'A', '1': 'B'},
#     'B': {'0': 'A', '1': 'C'},
#     'C': {'0': 'C', '1': 'C'},
# }
# start_state = 'A'
# final_states = ['C']
# draw_dfa(dfa, start_state, final_states)


def convert_multigraph_to_graph(M):
    G = nx.DiGraph() if M.is_directed() else nx.Graph()
    for u, v, data in M.edges(data=True):
        if G.has_edge(u, v):
            G[u][v]['label'].append(data['label'])
        else:
            G.add_edge(u, v, label=[data['label']])
    for u, v, data in G.edges(data=True):
        data['label'] = ', '.join(data['label'])  # Join list of labels into a string
    return G
