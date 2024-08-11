import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

# Create an empty directed graph
G = nx.DiGraph()

# Adding nodes (sections)
nodes = [
    "Entrance", "Produce", "Dairy", "Bakery", "Frozen",
    "Meat", "Canned Goods", "Beverages", "Snacks", "Cleaning Supplies",
    "Personal Care", "Bread", "Vegetables", "Fruits", "Deli",
    "Seafood", "Pasta", "Sauces", "Milk", "Cheese", "Billing Counter"
]
G.add_nodes_from(nodes)

# Adding directed edges (paths) with distances (bidirectional)
edges = [
    ("Entrance", "Produce", 2),
    ("Entrance", "Canned Goods", 4),
    ("Entrance", "Bread", 6),
    ("Entrance", "Pasta", 8),

    ("Produce", "Dairy", 1),
    ("Dairy", "Bakery", 1),
    ("Bakery", "Frozen", 1),
    ("Frozen", "Meat", 1),

    ("Meat", "Canned Goods", 5),#meat mapping
    ("Meat", "Beverages", 4),
    ("Meat", "Snacks", 3),
    ("Meat", "Cleaning Supplies", 2),
    ("Meat", "Personal Care", 1),
    ("Frozen", "Personal Care", 2),#frozen mapping
    ("Frozen", "Cleaning Supplies", 1),
    ("Frozen", "Snacks", 2),
    ("Frozen", "Beverages", 3),
    ("Frozen", "Canned Goods", 4),
    ("Bakery", "Personal Care", 3),#bakery mapping
    ("Bakery", "Cleaning Supplies", 2),
    ("Bakery", "Snacks", 1),
    ("Bakery", "Beverages", 2),
    ("Bakery", "Canned Goods", 3),
    ("Dairy", "Personal Care", 4),#dairy mapping
    ("Dairy", "Cleaning Supplies", 3),
    ("Dairy", "Snacks", 2),
    ("Dairy", "Beverages", 1),
    ("Dairy", "Canned Goods", 2),
    ("Produce", "Personal Care", 5),#produce mapping
    ("Produce", "Cleaning Supplies", 4),
    ("Produce", "Snacks", 3),
    ("Produce", "Beverages", 2),
    ("Produce", "Canned Goods", 1),

    ("Canned Goods", "Beverages", 1),
    ("Beverages", "Snacks", 1),
    ("Snacks", "Cleaning Supplies", 1),
    ("Cleaning Supplies", "Personal Care", 1),

    ("Bread", "Vegetables", 1),
    ("Vegetables", "Fruits", 1),
    ("Fruits", "Deli", 1),
    ("Deli", "Seafood", 1),

    ("Seafood", "Pasta", 5),#Seafood mapping
    ("Seafood", "Sauces", 4),
    ("Seafood", "Milk", 3),
    ("Seafood", "Cheese", 2),
    ("Deli", "Cheese", 1),#deli mapping
    ("Deli", "Milk", 2),
    ("Deli", "Sauces", 3),
    ("Deli", "Pasta", 4),
    ("Fruits", "Cheese", 2),#fruits mapping
    ("Fruits", "Milk", 1),
    ("Fruits", "Sauces", 2),
    ("Fruits", "Pasta", 3),
    ("Vegetables", "Cheese", 3),#Vegetables mapping
    ("Vegetables", "Milk", 2),
    ("Vegetables", "Sauces", 1),
    ("Vegetables", "Pasta", 2),
    ("Bread", "Cheese", 4),#Bread mapping
    ("Bread", "Milk", 3),
    ("Bread", "Sauces", 2),
    ("Bread", "Pasta", 1),

    ("Pasta", "Sauces", 1),
    ("Sauces", "Milk", 1),
    ("Milk", "Cheese", 1), 

    ("Personal Care", "Seafood", 4),
    ("Bread", "Canned Goods", 4),

    ("Billing Counter", "Cheese", 2),
    ("Billing Counter", "Seafood", 4),
    ("Billing Counter", "Personal Care", 6),
    ("Billing Counter", "Meat", 8)
]

# Add each edge in both directions
for u, v, w in edges:
    G.add_edge(u, v, weight=w)
    G.add_edge(v, u, weight=w)

# Updated shopping list
shopping_list = ["Bread", "Vegetables", "Cheese", "Snacks", "Frozen"]

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
    for i in range(len(full_path) - 1):
        path_length += nx.shortest_path_length(G, source=full_path[i], target=full_path[i+1], weight="weight")
    
    # If this path is shorter, update the minimum
    if path_length < min_path_length:
        min_path_length = path_length
        min_path = full_path

# Calculate the full optimal path using shortest paths between each pair of nodes in the min_path
optimal_path = []
for i in range(len(min_path) - 1):
    optimal_path += nx.shortest_path(G, source=min_path[i], target=min_path[i + 1], weight="weight")[:-1]
# Add the last node
optimal_path += [min_path[-1]]

# Create a subgraph for the optimal path
subgraph_edges = [(optimal_path[i], optimal_path[i+1]) for i in range(len(optimal_path) - 1)]
optimal_subgraph = G.edge_subgraph(subgraph_edges).copy()

# Define static positions manually
pos = {
    "Entrance": (0, 0),
    "Produce": (1, 1), # 1st row
    "Dairy": (2, 1), # 1st row
    "Bakery": (3, 1), # 1st row
    "Frozen": (4, 1), # 1st row
    "Meat": (5, 1), # 1st row
    "Canned Goods": (1, 2), # 2nd row
    "Beverages": (2, 2), # 2nd row
    "Snacks": (3, 2), # 2nd row
    "Cleaning Supplies": (4, 2), # 2nd row
    "Personal Care": (5, 2), # 2nd row
    "Bread": (1, 3), # 3rd row
    "Vegetables": (2, 3), # 3rd row
    "Fruits": (3, 3), # 3rd row
    "Deli": (4, 3), # 3rd row
    "Seafood": (5, 3), # 3rd row
    "Pasta": (1, 4), # 4th row
    "Sauces": (2, 4), # 4th row
    "Milk": (3, 4), # 4th row
    "Cheese": (4, 4), # 4th row
    "Billing Counter": (5, 5)
}

# Draw the entire graph with all possible routes
plt.figure(figsize=(14, 10))

# Draw the entire graph with directed edges
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, edge_color='lightgray', width=1.5, arrows=True, arrowstyle='-|>', arrowsize=20)

# Draw the optimal path
nx.draw(optimal_subgraph, pos, with_labels=True, node_color="lightgreen", node_size=800, font_size=10, edge_color='blue', width=2.5, arrows=True, arrowstyle='-|>', arrowsize=20)

# Highlight the 'Entrance' node with larger size
nx.draw_networkx_nodes(G, pos, nodelist=["Entrance"], node_color="lightcoral", node_size=1000)
nx.draw_networkx_labels(G, pos, labels={"Entrance": "Entrance"}, font_size=20, font_color="white", font_weight="bold")

# Set the figure title
plt.title("Optimal Path in the Store")

# Show the plot
plt.show()
