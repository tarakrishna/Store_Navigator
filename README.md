# Store Path Optimization App

This is a Python application developed using Streamlit that helps users find the optimal path through a store based on their shopping list. The app calculates the most efficient route to navigate the store from the entrance to the billing counter while ensuring all selected items are picked up along the way.

## Aim

The primary aim of this application is to assist shoppers in minimizing the time and distance spent walking through the store by providing the most efficient path based on the items in their shopping list. By mapping out the store sections and computing the shortest path, the app optimizes the shopping experience, making it more convenient and time-saving.

## Approach

### 1. **Graph Representation**
   - The store layout is modeled as a directed weighted graph using the NetworkX library.
   - Each node represents a section in the store, such as "Produce", "Bakery", etc.
   - The edges between nodes represent the paths between store sections, with weights corresponding to the distances between them.

### 2. **Optimal Path Calculation**
   - The application uses a greedy algorithm to calculate a near-optimal path.
   - Starting from the "Entrance", the algorithm iteratively selects the next closest section on the shopping list, minimizing the distance covered.
   - The path ends at the "Billing Counter" after all items in the shopping list have been picked up.
   - The final path is constructed using the shortest paths between the selected nodes.

### 3. **Graph Visualization**
   - The graph is visualized using Matplotlib, displaying the store layout and the optimal path.
   - Nodes corresponding to the shopping list items are highlighted in green, while the entrance and billing counter are highlighted in red.
   - Users can interactively view the entire graph, reveal the next or previous edges of the optimal path, and see the complete route.

## Features

- **User-friendly Interface**: The app features a simple and intuitive interface for selecting items and visualizing the optimal path.
- **Interactive Path Display**: Users can incrementally display the calculated path to understand the sequence of stops.
- **Graph Visualization**: The store layout and paths are clearly visualized, making it easy to follow the directions.

## Installation

To run the app locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/store-path-optimization.git
   cd store-path-optimization




