import networkx as nx
import matplotlib.pyplot as plt
import random


def load_graph(input_file):
    """
    Load a GraphML file into a NetworkX graph.

    Parameters:
    - input_file (str): The path to the GraphML file to load.

    Returns:
    - G (networkx.Graph): The loaded NetworkX graph.
    """
    return nx.read_graphml(input_file)


def generate_node_colors(G, attribute, color_map, default_color="gray"):
    """
    Generate a list of colors for nodes based on a specified attribute.

    Parameters:
    - G (networkx.Graph): The NetworkX graph.
    - attribute (str): The node attribute used for coloring 
                       (e.g., 'true_state' or 'state').
    - color_map (dict): A dictionary mapping attribute values to colors.
    - default_color (str): Color for nodes without the specified attribute.

    Returns:
    - list: A list of colors for each node based on the specified attribute.
    """
    return [
        color_map.get(G.nodes[node].get(attribute, default_color), default_color)
        for node in G.nodes()
    ]


def add_fraud_accomplice_edges(G, max_accomplice_edges=5):
    """
    Add edges between nodes labeled as 'Fraud' and randomly selected 'Accomplice' nodes.

    Parameters:
    - G (networkx.Graph): The NetworkX graph.
    - max_accomplice_edges (int): Maximum number of accomplices to connect 
                                  to each fraud node.
    """
    for node in G.nodes:
        if G.nodes[node].get("true_state") == "Fraud":
            accomplices = [
                n for n in G.nodes if G.nodes[n].get("true_state") == "Accomplice"
            ]
            accomplice_neighbors = random.sample(
                accomplices, min(max_accomplice_edges, len(accomplices))
            )
            for accomplice in accomplice_neighbors:
                if not G.has_edge(node, accomplice):
                    G.add_edge(node, accomplice)


def visualize_graph(G, attribute, color_map, subset_size=100, title="Graph Visualization"):
    """
    Visualize a subset of nodes in a graph with colors based on a specified node attribute.

    Parameters:
    - G (networkx.Graph): The NetworkX graph.
    - attribute (str): The node attribute used for coloring (e.g., 'true_state' or 'state').
    - color_map (dict): A dictionary mapping attribute values to colors.
    - subset_size (int): Number of nodes to visualize.
    - title (str): Title for the visualization.
    """
    subset = G.subgraph(list(G.nodes())[:subset_size])
    pos = nx.spring_layout(subset)

    # Generate node colors based on the specified attribute
    node_colors = [
        color_map.get(G.nodes[node].get(attribute, "gray"), "gray")
        for node in subset.nodes()
    ]

    plt.figure(figsize=(8, 8))
    nx.draw(
        subset,
        pos,
        node_color=node_colors,
        with_labels=True,
        node_size=50,
        font_size=8
    )
    plt.title(title)
    plt.show()


def save_graph(G, output_file):
    """
    Save the NetworkX graph in GraphML format.

    Parameters:
    - G (networkx.Graph): The NetworkX graph.
    - output_file (str): The path to save the GraphML file.
    """
    nx.write_graphml(G, output_file)
    print(f"Graph saved with additional edges to {output_file}")


# Main execution block
if __name__ == "__main__":
    # Define parameters and file paths
    input_file = "synthetic_network.graphml"
    output_file = "synthetic_network_with_true_states_enhanced.graphml"
    color_map = {"Fraud": "red", "Accomplice": "orange", "Honest": "green"}

    # Load the graph
    G = load_graph(input_file)

    # Generate color mappings based on `true_state` and `state` attributes
    node_colors_true_state = generate_node_colors(G, "true_state", color_map)
    node_colors_state = generate_node_colors(G, "state", color_map)

    # Optional: Add edges between 'Fraud' and 'Accomplice' nodes
    add_fraud_accomplice_edges(G)

    # Visualize the graph based on `true_state
    subset_size = 100  # Visualize a subset of 100 nodes for clarity
    fig, (ax1) = plt.subplots(1, figsize=(8, 8))

    # Visualization for `true_state`
    subset_true_state = G.subgraph(list(G.nodes())[:subset_size])
    pos = nx.spring_layout(subset_true_state)
    nx.draw(
        subset_true_state,
        pos,
        ax=ax1,
        node_color=[
            color_map.get(G.nodes[node].get("true_state", "gray"), "gray")
            for node in subset_true_state.nodes()
        ],
        with_labels=True,
        node_size=50,
        font_size=8
    )
    ax1.set_title("Synthetic Network with Roles Based on true_state Attribute")

    plt.show()

    # Save the modified graph with additional edges
    save_graph(G, output_file)
