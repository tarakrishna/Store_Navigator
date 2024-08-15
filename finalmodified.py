import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from itertools import permutations
import streamlit as st

# Function to calculate the optimal path
def calculate_optimal_path(G, shopping_list):
    nodes_to_visit = ["Entrance"] + shopping_list + ["Billing Counter"]
    
    # Initialize variables
    min_path = None
    min_path_length = float('inf')
    
    # Use a greedy approach to find a near-optimal path
    current_node = "Entrance"
    path = [current_node]
    total_length = 0
    remaining_nodes = shopping_list.copy()
    
    while remaining_nodes:
        min_edge = None
        min_weight = float('inf')
        for next_node in remaining_nodes:
            try:
                edge_weight = nx.shortest_path_length(G, source=current_node, target=next_node, weight="weight")
                if edge_weight < min_weight:
                    min_weight = edge_weight
                    min_edge = next_node
            except nx.NetworkXNoPath:
                continue
        
        if min_edge is None:
            raise ValueError("No valid path found from 'Entrance' to 'Billing Counter' with the given shopping list.")
        
        path.append(min_edge)
        total_length += min_weight
        remaining_nodes.remove(min_edge)
        current_node = min_edge

    path.append("Billing Counter")
    
    # Construct the full path using the shortest paths between the nodes
    optimal_path = []
    for i in range(len(path) - 1):
        try:
            optimal_path += nx.shortest_path(G, source=path[i], target=path[i + 1], weight="weight")[:-1]
        except nx.NetworkXNoPath:
            continue
    optimal_path += [path[-1]]
    
    return optimal_path


# Function to draw the graph with the current number of edges displayed
def draw_graph_with_edges(G, pos, optimal_path, num_edges_displayed, show_full_graph=False):
    plt.figure(figsize=(14, 10))
    
    if show_full_graph:
        nodes_to_draw = list(set(G.nodes()) - {"a", "b", "c", "d", "o", "p", "q", "r", "e", "m", "n", "f", "g", "h", "i", "j", "k", "l", "s" , "t", "Entrance", "Billing Counter"} )
        nx.draw(G.subgraph(nodes_to_draw), pos, nodelist=nodes_to_draw, with_labels=True, node_color="lightblue", node_size=500, font_size=10, edge_color='lightgray', width=1.5, arrows=True, arrowstyle='-|>', arrowsize=20)
        edges_to_draw = list(zip(optimal_path[:-1], optimal_path[1:]))[:num_edges_displayed]
        nx.draw_networkx_edges(G, pos, edgelist=edges_to_draw, edge_color='blue', width=2.5, arrows=True, arrowstyle='-|>', arrowsize=20)
        shopping_list_nodes = set(shopping_list)
        nx.draw_networkx_nodes(G, pos, nodelist=shopping_list_nodes, node_color="lightgreen", node_size=800)
        nx.draw_networkx_nodes(G, pos, nodelist=["Entrance", "Billing Counter"], node_color="lightcoral", node_size=1000)
        nx.draw_networkx_labels(G, pos, labels={"Entrance": "Entrance", "Billing Counter": "Billing Counter"}, font_size=13, font_color="black", font_weight="bold")
        rect_x = 1.05
        rect_y = 2.02
        rect_width = 3.95
        rect_height = 0.37
        rect = patches.Rectangle((rect_x, rect_y), linewidth=1, edgecolor='grey', facecolor='grey', width=rect_width, height=rect_height)
        plt.gca().add_patch(rect)
        rect_x = -1.0
        rect_y = 0.0
        rect_width = 0.95
        rect_height = 4.37
        rect = patches.Rectangle((rect_x, rect_y), linewidth=1, edgecolor='grey', facecolor='grey', width=rect_width, height=rect_height)
        plt.gca().add_patch(rect)
        rect_x = -0.05
        rect_y = 0.0
        rect_width = 7.1
        rect_height = 0.97
        rect = patches.Rectangle((rect_x, rect_y), linewidth=1, edgecolor='grey', facecolor='grey', width=rect_width, height=rect_height)
        plt.gca().add_patch(rect)   
        plt.gca().add_patch(rect)
        rect_x = -0.05
        rect_y = 3.4
        rect_width = 7.1
        rect_height = 0.97
        rect = patches.Rectangle((rect_x, rect_y), linewidth=1, edgecolor='grey', facecolor='grey', width=rect_width, height=rect_height)
        plt.gca().add_patch(rect) 
        plt.gca().add_patch(rect)
        rect_x = 7
        rect_y = 0
        rect_width = 1
        rect_height = 4.37
        rect = patches.Rectangle((rect_x, rect_y), linewidth=1, edgecolor='grey', facecolor='grey', width=rect_width, height=rect_height)
        plt.gca().add_patch(rect) 
        plt.title("Optimal Path in the Store - Shopping List Highlighted with Rectangle")
        plt.title("Store Layout with Optimal Path Highlighted")

    else:
        nodes_to_draw = list(set(G.nodes()) - {"a", "b", "c", "d", "o", "p", "q", "r", "e", "m", "n", "f", "g", "h", "i", "j", "k", "l", "s" , "t", "Entrance", "Billing Counter"} )
        nx.draw(G.subgraph(nodes_to_draw), pos, nodelist=nodes_to_draw, with_labels=True, node_color="lightblue", node_size=500, font_size=10, edge_color='lightgray', width=1.5, arrows=True, arrowstyle='-|>', arrowsize=20)
        edges_to_draw = list(zip(optimal_path[:-1], optimal_path[1:]))[:num_edges_displayed]
        nx.draw_networkx_edges(G, pos, edgelist=edges_to_draw, edge_color='blue', width=2.5, arrows=True, arrowstyle='-|>', arrowsize=20)
        shopping_list_nodes = set(shopping_list)
        nx.draw_networkx_nodes(G, pos, nodelist=shopping_list_nodes, node_color="lightgreen", node_size=800)
        nx.draw_networkx_nodes(G, pos, nodelist=["Entrance", "Billing Counter"], node_color="lightcoral", node_size=1000)
        nx.draw_networkx_labels(G, pos, labels={"Entrance": "Entrance", "Billing Counter": "Billing Counter"}, font_size=13, font_color="black", font_weight="bold")
        rect_x = 1.05
        rect_y = 2.02
        rect_width = 3.95
        rect_height = 0.37
        rect = patches.Rectangle((rect_x, rect_y), linewidth=1, edgecolor='grey', facecolor='grey', width=rect_width, height=rect_height)
        plt.gca().add_patch(rect)
        rect_x = -1.0
        rect_y = 0.0
        rect_width = 0.95
        rect_height = 4.37
        rect = patches.Rectangle((rect_x, rect_y), linewidth=1, edgecolor='grey', facecolor='grey', width=rect_width, height=rect_height)
        plt.gca().add_patch(rect)
        rect_x = -0.05
        rect_y = 0.0
        rect_width = 7.1
        rect_height = 0.97
        rect = patches.Rectangle((rect_x, rect_y), linewidth=1, edgecolor='grey', facecolor='grey', width=rect_width, height=rect_height)
        plt.gca().add_patch(rect)   
        plt.gca().add_patch(rect)
        rect_x = -0.05
        rect_y = 3.4
        rect_width = 7.1
        rect_height = 0.97
        rect = patches.Rectangle((rect_x, rect_y), linewidth=1, edgecolor='grey', facecolor='grey', width=rect_width, height=rect_height)
        plt.gca().add_patch(rect) 
        plt.gca().add_patch(rect)
        rect_x = 7
        rect_y = 0
        rect_width = 1
        rect_height = 4.37
        rect = patches.Rectangle((rect_x, rect_y), linewidth=1, edgecolor='grey', facecolor='grey', width=rect_width, height=rect_height)
        plt.gca().add_patch(rect) 
        plt.title("Optimal Path in the Store - Shopping List Highlighted with Rectangle")

    st.pyplot(plt)

# Streamlit app
st.title("Store Path Optimization")

# Define the nodes
nodes = [
    "Entrance", "Produce", "a", "b", "c", "d", "e", "f", "g", "h", "i" , "j", "k", "l", "m", "n","o", "p", "q","r","s","t", "Dairy", "Bakery", "Frozen",
    "Meat", "Canned Goods", "Beverages", "Snacks", "Cleaning Supplies",
    "Personal Care", "Bread", "Vegetables", "Fruits", "Deli","electrical","Clothing",
    "Seafood", "Pasta", "Sauces", "Milk", "Cheese", "Billing Counter", "Hardware","Veganfood","Decor","Petfood","Utensils"
]

# Dropdown menu for shopping list
shopping_list = st.multiselect("Select items to add to your shopping list:", list(set(nodes) - set(["a", "b", "c", "d", "e", "f", "g", "h", "i" , "j", "k", "l", "m", "n","o", "p", "q","r","s","t","Entrance", "Billing Counter"])))

if 'num_edges_displayed' not in st.session_state:
    st.session_state.num_edges_displayed = 0
    st.session_state.optimal_path = []
    st.session_state.G = None
    st.session_state.pos = None
    st.session_state.show_full_graph = False
    st.session_state.previous_num_edges_displayed = 0

if st.button("Generate Optimal Path"):
    G = nx.DiGraph()

    edges = [
        ("Entrance", "m", 1),
        ("m", "a", 1),
        ("m", "o" ,0.5),
        ("o","p",0.5),
        ("o", "Canned Goods", 1),
        ("p","Bread", 1),
        ("p","n",0.5),
        ("Produce", "a", 0.5),
        ("a", "b", 1),
        ("a", "Canned Goods", 0.5),
        ("b", "Dairy", 0.5),
        ("b", "Beverages", 0.5),
        ("b","c",1),
        ("c", "Bakery", 0.5),
        ("c","Snacks", 0.5),
        ("c","d",1),
        ("d","Frozen", 0.5),
        ("d","Cleaning Supplies",0.5),
        ("d","e",1),
        ("e","Meat",0.5),
        ("e","Personal Care", 0.5),
        ("e","f",1),
        ("g","h",1),
        ("h","Seafood",0.5),
        ("h","Hardware",0.5),
        ("h","i",1),
        ("i","Cheese",0.5),
        ("i","Deli",0.5),
        ("i","j",1),
        ("j","Milk",0.5),
        ("j","Fruits",0.5),
        ("j","k",1),
        ("k","Sauces",0.5),
        ("k", "Vegetables", 0.5),
        ("k","l",1),
        ("l", "Pasta", 0.5),
        ("l", "Bread", 0.5),
        ("l", "n", 1),
        ("f","q",0.5),
        ("q","r",0.5),
        ("r","g",0.5),
        ("q","Personal Care",1),
        ("r","Seafood",1),
        ("n", "Billing Counter",1),
        ("s", "Veganfood",1),
        ("q", "Decor", 1),
        ("r", "Petfood", 1),
        ("t", "Utensils",1),
        ("g","t",0.5),
        ("f", "s", 0.5),
        ("f", "electrical", 1),
        ("g", "Clothing", 1)
    ]

    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
        G.add_edge(v, u, weight=w)

    pos = {
        "Entrance": (0, 1),
        "Produce": (1, 1),
        "a": (1, 1.5),
        "b": (2, 1.5),
        "c" : (3,1.5),
        "d" : (4,1.5),
        "e" : (5,1.5),
        "f" : (6,1.5),
        "g" : (6,2.9),
        "h" : (5,2.9),
        "i" : (4,2.9),
        "j" : (3,2.9),
        "k" : (2,2.9),
        "l" : (1,2.9),
        "o" : (0,2),
        "p" : (0,2.4),
        "q" : (6,2),
        "r" : (6,2.4),
        "Dairy": (2, 1),
        "Bakery": (3, 1),
        "Frozen": (4, 1),
        "Meat": (5, 1),
        "Canned Goods": (1, 2),
        "Beverages": (2, 2),
        "Snacks": (3, 2),
        "Cleaning Supplies": (4, 2),
        "Personal Care": (5, 2),
        "Bread": (1, 2.4),
        "Vegetables": (2, 2.4),
        "Fruits": (3, 2.4),
        "Deli": (4, 2.4),
        "Seafood": (5, 2.4),
        "Pasta": (1, 3.4),
        "Sauces": (2, 3.4),
        "Milk": (3, 3.4),
        "Cheese": (4, 3.4),
        "Billing Counter": (0, 3.4),
        "Hardware" : (5,3.4),
        "m" : (0,1.5),
        "n" : (0,2.9),
        "Veganfood" :(7,1),
        "Decor" : (7,2),
        "Petfood" : (7,2.4),
        "Utensils" : (7,3.4),
        "s" : (6,1),
        "t" : (6,3.4),
        "electrical" : (7,1.5),
        "Clothing" : (7,2.9)
    }

    optimal_path = calculate_optimal_path(G, shopping_list)

    st.session_state.G = G
    st.session_state.pos = pos
    st.session_state.optimal_path = optimal_path
    st.session_state.num_edges_displayed = 0
    st.session_state.show_full_graph = False
    st.session_state.previous_num_edges_displayed = 0

    draw_graph_with_edges(G, pos, optimal_path, st.session_state.num_edges_displayed)

# Button to toggle entire graph view
if st.button("Show Entire Graph"):
    if st.session_state.show_full_graph:
        st.session_state.show_full_graph = False
        st.session_state.num_edges_displayed = st.session_state.previous_num_edges_displayed
        draw_graph_with_edges(st.session_state.G, st.session_state.pos, st.session_state.optimal_path, st.session_state.num_edges_displayed)
    else:
        st.session_state.previous_num_edges_displayed = st.session_state.num_edges_displayed
        st.session_state.show_full_graph = True
        st.session_state.num_edges_displayed = len(st.session_state.optimal_path) - 1
        draw_graph_with_edges(st.session_state.G, st.session_state.pos, st.session_state.optimal_path, st.session_state.num_edges_displayed, show_full_graph=True)

# Button to show the next edge in the optimal path
if st.button("Show Next Edge"):
    if st.session_state.num_edges_displayed < len(st.session_state.optimal_path) - 1:
        st.session_state.num_edges_displayed += 1
        draw_graph_with_edges(st.session_state.G, st.session_state.pos, st.session_state.optimal_path, st.session_state.num_edges_displayed)

# Button to show the previous edge in the optimal path
if st.button("Show Previous Edge"):
    if st.session_state.num_edges_displayed > 0:
        st.session_state.num_edges_displayed -= 1
        draw_graph_with_edges(st.session_state.G, st.session_state.pos, st.session_state.optimal_path, st.session_state.num_edges_displayed)