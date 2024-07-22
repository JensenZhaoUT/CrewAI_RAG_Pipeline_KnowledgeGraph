from langchain.tools import tool
import json
import os
from typing import ClassVar, List, Dict
import networkx as nx
import matplotlib.pyplot as plt

class KnowledgeGraphBuilder:
    BuildGraph: ClassVar

    @tool("build_knowledge_graph")
    @staticmethod
    def BuildGraph(retrieved_file_path: str, path_to_save_dir: str) -> str:
        """
        Build a knowledge graph based on the retrieved file and save the graph to the save directory.

        Args:
            retrieved_file_path (str): The path to the JSON file containing the retrieved information.
            path_to_save_dir (str): The directory where the knowledge graph will be saved.

        Returns:
            str: The path to the saved knowledge graph image.

        Raises:
            FileNotFoundError: If the specified JSON file does not exist.
        """
        # Clean up file path and save directory inputs
        retrieved_file_path = retrieved_file_path.strip('"')
        path_to_save_dir = path_to_save_dir.strip('"')
        print(f"KnowledgeGraphBuilder received cleaned file path: {retrieved_file_path}")
        print(f"KnowledgeGraphBuilder received cleaned save directory: {path_to_save_dir}")

        # Check if file exists
        if not os.path.exists(retrieved_file_path):
            print(f"DEBUG: os.path.exists({retrieved_file_path}) -> {os.path.exists(retrieved_file_path)}")
            raise FileNotFoundError(f"File {retrieved_file_path} not found.")
        
        # Check if save directory exists, create if it does not
        if not os.path.exists(path_to_save_dir):
            os.makedirs(path_to_save_dir)
        
        # Load the JSON data
        with open(retrieved_file_path, 'r') as file:
            data = json.load(file)

        # Create a directed graph
        G = nx.DiGraph()

        # Populate the graph with nodes and edges
        for table_name, table_data in data.items():
            headers = table_data.get("headers", [])
            rows = table_data.get("rows", [])
            for row in rows:
                for i, header in enumerate(headers):
                    if i < len(row):
                        G.add_node(row[i])
                        if i > 0:
                            G.add_edge(row[i-1], row[i])
        
        # Define the save path for the knowledge graph image
        graph_image_path = os.path.join(path_to_save_dir, "knowledge_graph.png")
        
        # Draw the graph
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold", arrows=True)
        plt.title("Knowledge Graph")
        plt.savefig(graph_image_path)
        plt.close()

        print(f"Knowledge graph saved to: {graph_image_path}")

        return graph_image_path
