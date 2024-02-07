import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt, animation
import numpy as np
def add_mutant_node(G,   percentage=0.2):
    """
    Add node to the network according to the method supplied. This new node may
    be added randomly, preferentially based on degree, or using insights about
    empirical distributions of protein-specific interaction patterns (here
    named 'bio_smart', 'random', and 'degree').

    Params
    ------
    G (nx.Graph):
        the (protein-protein interaction) network in question.

    m (int):
        the number of edges that each new node brings to the network.

    method (str):
        the method of node-addition in question. can be any of the following:
            - 'random': adds node's edges randomly.
            - 'degree': adds edges preferentially based on degree.
            - 'bio_smart': adds edges based on gene_expression data.

    alpha (float):
        in case the method=='degree', alpha tunes the preferential attachment
        exponent, which makes node_i more / less likely to attaching its m
        edges to high-degree nodes.

    Returns
    -------
    G (nx.Graph):
        the graph with nodes added.

    """


    nodes = list(G.nodes())
    N = len(nodes)
    probs = [1 / N for i in range(N)]
    eijs = np.random.choice(nodes, size=(1,), replace=False, p=probs)

    #duplicate_node = G.nodes[eijs[0]].copy()
    nchange = int(percentage*len(G.edges(eijs[0])))
    nchange = np.max([1,nchange])
    old_edgelen= np.max([len(list(G.edges(eijs[0]))),1])
        
    new_node_id = N 
    G.add_node(str(new_node_id))
    new_edges = []
    for edge in G.edges(eijs[0]):
        new_edge = list(edge)
        new_edge[0] = str(new_node_id)

        new_edge = tuple(new_edge)
        new_edges.append(new_edge)

    G.add_edges_from(new_edges)
    
    
    for i in range(nchange):
        edge_toremove = np.random.randint(len(list(G.edges(str(new_node_id)))), size=1)
        u=list(G.edges(str(new_node_id)))[int(edge_toremove)][0]
        v=list(G.edges(str(new_node_id)))[int(edge_toremove)][1]
        G.remove_edge(u,v)
    edges_to_add = [(str(new_node_id), np.random.choice(nodes, replace=False, p=probs)) for _ in range(nchange)]
    G.add_edges_from(edges_to_add)
        
    

    #np.random.randint(len(sl), size=1)
    #edges_to_remove = np.random.choice(list(G.edges(new_node_id)), size=(len(list(G.edges(new_node_id)))), replace=False)
    
    #G.remove_edges_from(edges_to_remove)




    return G
# Create a figure and axis for the plot
fig, ax = plt.subplots()

# Function to update the plot with the current state of the graph
"""def update(frame):
    
    ax.clear()
    for i in range(10):
        new_G = add_mutant_node(new_G,0.2)  # Add 5 nodes at each step (adjust as needed)
        pos = nx.spring_layout(new_G)
    return new_G

def diffuse_anim( nb_frames=50):
    G = nx.read_graphml('../data/G_sce.graphml')

    pos = nx.spring_layout(G)
    G1 = nx.erdos_renyi_graph(10,nx.density(G))
    relabel_dict = {node: str(node+len(G.nodes)) for node in G1.nodes}
    G1 = nx.relabel_nodes(G1, relabel_dict)
    new_G = nx.compose(G, G1)

    pos = nx.spring_layout(new_G)
    fig = plt.figure()
    nx.draw_networkx(new_G, pos, node_size=30, node_color='b')
    ani=FuncAnimation(fig, update, frames=range(nb_frames))
    ani.save('animation_1.gif', writer='imagemagick')
    plt.show()
    return ani"""

#anim=diffuse_anim()

fig = plt.figure()
G0 = nx.read_graphml('../data/G_sce.graphml')
G=G0
pos = nx.spring_layout(G)
for i in range(4):
    G1 = nx.erdos_renyi_graph(30,nx.density(G0))
    relabel_dict = {node: str(node+len(G.nodes)) for node in G1.nodes}
    G1 = nx.relabel_nodes(G1, relabel_dict)
    G = nx.compose(G, G1)
new_G=G
pos = nx.spring_layout(new_G)
cmap3 = plt.cm.Set2
import matplotlib
cmap = matplotlib.cm.get_cmap('tab20')

color_intervals = np.linspace(0,1,10) # for 13 colors
colors_tab = []
for value in color_intervals:
    colors_tab.append(cmap(value))

from networkx.algorithms.community import greedy_modularity_communities
communities = greedy_modularity_communities(new_G, weight="weight")
def animate(frame,new_G):
    fig.clear()
    new_G = add_mutant_node(new_G,0.3)  # Add 5 nodes at each step (adjust as needed)
    pos = nx.kamada_kawai_layout(new_G)
    partition_human = greedy_modularity_communities(new_G, weight="weight")
    community_color_map = []
    for node in new_G.nodes:
        for idx,community in enumerate(partition_human):
            if node in community:
                #print(node,idx)
                community_color_map.append(colors_tab[idx])
   
    nx.draw(new_G,pos=pos, node_color=community_color_map, node_size=10,
                           alpha=0.4, width=2)
"""ani = animation.FuncAnimation(fig, animate, frames=200, interval=1,  repeat=False,  fargs=[new_G])
ani.save("anim.gif")
plt.show()
fig = plt.figure()"""

def animate2(frame,new_G):
    fig.clear()
    new_G = add_mutant_node(new_G, 0.3)  # Add 5 nodes at each step (adjust as needed)
    edges = []
    n=list([new_G.nodes][0])
    for i in range(len([new_G.nodes][0])):

        edges.append(len(new_G.edges([n[i]])))
    plt.hist( edges)
   

ani2= animation.FuncAnimation(fig, animate2, frames=300, interval=1,  repeat=False,  fargs=[new_G])
ani2.save("anim2.gif")
plt.show()