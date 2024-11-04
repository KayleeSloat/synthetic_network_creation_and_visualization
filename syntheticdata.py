import networkx as nx
import random


def generate_synthetic_network(
    num_nodes=7000,
    target_edges=30000,
    initial_belief=None,
    state_distribution=None,
    output_file="synthetic_network.graphml"
):
    """
    Generates a synthetic network for fraud detection analysis and saves it to a specified file.

    Parameters:
    - num_nodes: int, the number of nodes in the network.
    - target_edges: int, the desired number of edges in the network.
    - initial_belief: dict, initial belief probabilities for each state (Fraud, Accomplice, Honest).
    - state_distribution: dict, target distribution for the true states of nodes.
    - output_file: str, path to save the generated GraphML file.
    """
    # Default parameter setup
    if initial_belief is None:
        initial_belief = {"Fraud": 1 / 3, "Accomplice": 1 / 3, "Honest": 1 / 3}
    if state_distribution is None:
        state_distribution = {"Fraud": 0.1, "Accomplice": 0.2, "Honest": 0.7}

    # Set random seed for reproducibility
    random.seed(42)

    # Step 1: Generate Barabási-Albert graph
    m = max(1, target_edges // num_nodes)  # Parameter for edge creation in Barabási-Albert model
    G = nx.barabasi_albert_graph(n=num_nodes, m=m)

    # Step 2: Add random edges to meet the target edge count
    existing_edges = set(G.edges())
    nodes_list = list(G.nodes())
    while G.number_of_edges() < target_edges:
        node1, node2 = random.sample(nodes_list, 2)
        if (node1, node2) not in existing_edges and (node2, node1) not in existing_edges:
            G.add_edge(node1, node2, weight=random.uniform(0.1, 1.0))
            existing_edges.add((node1, node2))

    # Step 3: Assign true states and initial beliefs to each node
    state_counts = {"Fraud": 0, "Accomplice": 0, "Honest": 0}
    for node in G.nodes():
        true_state = random.choices(
            ["Fraud", "Accomplice", "Honest"],
            weights=[
                state_distribution["Fraud"],
                state_distribution["Accomplice"],
                state_distribution["Honest"]
            ],
            k=1
        )[0]
        G.nodes[node]["true_state"] = true_state
        G.nodes[node]["belief_fraud"] = initial_belief["Fraud"]
        G.nodes[node]["belief_accomplice"] = initial_belief["Accomplice"]
        G.nodes[node]["belief_honest"] = initial_belief["Honest"]
        G.nodes[node]["state"] = random.choice(["Fraud", "Accomplice", "Honest"])
        state_counts[true_state] += 1

    # Step 4: Print the target vs. generated distribution for verification
    total_nodes = sum(state_counts.values())
    print(f"Target distribution: {state_distribution}")
    print(
        f"Generated distribution: {{'Fraud': {state_counts['Fraud'] / total_nodes:.2%}, "
        f"'Accomplice': {state_counts['Accomplice'] / total_nodes:.2%}, "
        f"'Honest': {state_counts['Honest'] / total_nodes:.2%}}}"
    )

    # Step 5: Add metadata to the graph for reference
    G.graph["num_nodes"] = num_nodes
    G.graph["target_edges"] = target_edges
    G.graph["initial_belief"] = str(initial_belief)  # Convert to string for GraphML compatibility
    G.graph["state_distribution"] = str(state_distribution)

    # Step 6: Output graph characteristics and save
    avg_degree = sum(dict(G.degree()).values()) / num_nodes
    print(f"Average degree: {avg_degree:.2f}")
    print(f"Generated synthetic graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges (target: {target_edges} edges).")
    print("Example node data with true states (first 5 nodes):")
    for node, data in list(G.nodes(data=True))[:5]:
        print(f"Node {node}: {data}")

    # Save the generated graph to a file
    nx.write_graphml(G, output_file)
    print(f"Synthetic graph saved to {output_file}")


# Example usage of generate_synthetic_network function
if __name__ == "__main__":
    generate_synthetic_network()
