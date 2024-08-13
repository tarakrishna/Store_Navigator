import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from itertools import permutations
import streamlit as st

# Function to calculate the optimal path
def calculate_optimal_path(G, shopping_list):
    # Include Entrance at the start and Billing Counter at the end
    nodes_to_visit = ["Entrance"] + shopping_list + ["Billing Counter"]

    # Calculate all permutations of the shopping list (excluding Entrance and Billing Counter)
    permutations_of_stops = permutations(shopping_list)

    # Find the optimal path by checking each permutation
    min_path = None
    min_path_length = float('inf')

    for perm in permutations_of_stops:
        # Create a full path: Entrance -> perm -> Billing Counter
        full_path = ["Entrance"] + list(perm) + ["Billing Counter"]
        
        # Calculate the total path length
        path_length = 0
        try:
            for i in range(len(full_path) - 1):
                path_length += nx.shortest_path_length(G, source=full_path[i], target=full_path[i+1], weight="weight")
        except nx.NetworkXNoPath:
            continue  # Skip this permutation if any path is not reachable
        
        # If this path is shorter, update the minimum
        if path_length < min_path_length:
            min_path_length = path_length
            min_path = full_path

    if min_path is None:
        raise ValueError("No valid path found from 'Entrance' to 'Billing Counter' with the given shopping list.")

    # Calculate the full optimal path using shortest paths between each pair of nodes in the min_path
    optimal_path = []
    for i in range(len(min_path) - 1):
        try:
            optimal_path += nx.shortest_path(G, source=min_path[i], target=min_path[i + 1], weight="weight")[:-1]
        except nx.NetworkXNoPath:
            continue  # Skip this path segment if not reachable
    # Add the last node
    optimal_path += [min_path[-1]]

    return optimal_path

# Function to draw the graph with the current number of edges displayed
def draw_graph_with_edges(G, pos, optimal_path, num_edges_displayed, show_full_graph=False):
    plt.figure(figsize=(14, 10))
    
    # Draw the entire graph with all nodes and edges
    if show_full_graph:
        # Draw all nodes and edges
        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, edge_color='lightgray', width=1.5, arrows=True, arrowstyle='-|>', arrowsize=20)

        # Draw the optimal path in a different color
        optimal_edges = list(zip(optimal_path[:-1], optimal_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=optimal_edges, edge_color='blue', width=2.5, arrows=True, arrowstyle='-|>', arrowsize=20)
        
        # Highlight the nodes in the optimal path
        shopping_list_nodes = set(optimal_path)
        nx.draw_networkx_nodes(G, pos, nodelist=shopping_list_nodes, node_color="lightgreen", node_size=800)

        # Highlight the 'Entrance' and 'Billing Counter' nodes with a larger size
        nx.draw_networkx_nodes(G, pos, nodelist=["Entrance", "Billing Counter"], node_color="lightcoral", node_size=1000)
        nx.draw_networkx_labels(G, pos, labels={"Entrance": "Entrance", "Billing Counter": "Billing Counter"}, font_size=20, font_color="white", font_weight="bold")
        
        # Set the figure title
        plt.title("Store Layout with Optimal Path Highlighted")

    else:
        # Draw the graph with edges up to the current step
        nodes_to_draw = list(set(G.nodes()) - {"a", "b", "c", "d", "o", "p", "q", "r", "e", "m", "n", "f", "g", "h", "i", "j", "k", "l"})
        nx.draw(G.subgraph(nodes_to_draw), pos, nodelist=nodes_to_draw, with_labels=True, node_color="lightblue", node_size=500, font_size=10, edge_color='lightgray', width=1.5, arrows=True, arrowstyle='-|>', arrowsize=20)
        
        # Draw all edges (in light gray)
        nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=1.5, arrows=True, arrowstyle='-|>', arrowsize=20)

        # Draw the edges up to the current step
        edges_to_draw = list(zip(optimal_path[:-1], optimal_path[1:]))[:num_edges_displayed]
        nx.draw_networkx_edges(G, pos, edgelist=edges_to_draw, edge_color='blue', width=2.5, arrows=True, arrowstyle='-|>', arrowsize=20)

        # Highlight the nodes in the shopping list
        shopping_list_nodes = set(optimal_path)
        nx.draw_networkx_nodes(G, pos, nodelist=shopping_list_nodes, node_color="lightgreen", node_size=800)

        # Highlight the 'Entrance' and 'Billing Counter' nodes with a larger size
        nx.draw_networkx_nodes(G, pos, nodelist=["Entrance", "Billing Counter"], node_color="lightcoral", node_size=1000)
        nx.draw_networkx_labels(G, pos, labels={"Entrance": "Entrance", "Billing Counter": "Billing Counter"}, font_size=20, font_color="white", font_weight="bold")

        # Draw a black filled rectangle
        rect_x = 1.0  # x-coordinate of the bottom left corner
        rect_y = 2.0  # y-coordinate of the bottom left corner
        rect_width = 4  # width of the rectangle
        rect_height = 0.4  # height of the rectangle
        rect = patches.Rectangle((rect_x, rect_y), linewidth=1, edgecolor='black', facecolor='black', width=rect_width, height=rect_height)
        plt.gca().add_patch(rect)

        # Set the figure title
        plt.title("Optimal Path in the Store - Shopping List Highlighted with Rectangle")

    # Display the plot in Streamlit
    st.pyplot(plt)


# Streamlit app
st.title("Store Path Optimization")

# Input for shopping list
shopping_list_input = st.text_input("Enter your shopping list (comma separated):", "Pasta")
shopping_list = [item.strip() for item in shopping_list_input.split(",")]

# Session state to track the number of edges displayed
if 'num_edges_displayed' not in st.session_state:
    st.session_state.num_edges_displayed = 0
    st.session_state.optimal_path = []
    st.session_state.G = None
    st.session_state.pos = None
    st.session_state.show_full_graph = False

# Button to calculate and reset the optimal path
if st.button("Generate Optimal Path"):
    # Create an empty directed graph
    G = nx.DiGraph()

    # Adding nodes (sections)
    nodes = [
        "Entrance", "Produce", "a", "b", "c", "d", "e", "f", "g", "h", "i" , "j", "k", "l", "m", "n","o", "p", "q","r", "Dairy", "Bakery", "Frozen",
        "Meat", "Canned Goods", "Beverages", "Snacks", "Cleaning Supplies",
        "Personal Care", "Bread", "Vegetables", "Fruits", "Deli",
        "Seafood", "Pasta", "Sauces", "Milk", "Cheese", "Billing Counter", "Condom"
    ]
    G.add_nodes_from(nodes)

    # Adding directed edges (paths) with distances (bidirectional)
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
        ("Canned Goods", "Bread", 0.4),
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
        ("h","Condom",0.5),
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
        ("n", "Billing Counter",1)
    ]

    # Add each edge in both directions
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
        G.add_edge(v, u, weight=w)

    # Define positions for nodes
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
        "Condom" : (5,3.4),
        "m" : (0,1.5),
        "n" : (0,2.9)
    }

    # Calculate optimal path
    optimal_path = calculate_optimal_path(G, shopping_list)

    # Store graph and positions in session state
    st.session_state.G = G
    st.session_state.pos = pos
    st.session_state.optimal_path = optimal_path

    # Reset number of edges displayed
    st.session_state.num_edges_displayed = 0
    st.session_state.show_full_graph = False

    # Display initial graph
    draw_graph_with_edges(G, pos, optimal_path, st.session_state.num_edges_displayed)

# Button to show the entire graph
if st.button("Show Entire Graph"):
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
