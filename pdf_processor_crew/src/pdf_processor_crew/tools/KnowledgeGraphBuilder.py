from langchain.tools import tool
import json
import os
from typing import ClassVar
import networkx as nx
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Download stopwords if not already downloaded
nltk.download('punkt')
nltk.download('stopwords')

class KnowledgeGraphBuilder:
    BuildGraph: ClassVar

    @tool("build_knowledge_graph")
    @staticmethod
    def BuildGraph(user_query: str, parsed_tables: str, path_to_save_dir: str) -> str:
        """
        Build a knowledge graph based on the retrieved file and save the graph to the save directory.

        Args:
            user_query (str): The user's query.
            parsed_tables (str): The path to the JSON file containing the parsed tables.
            path_to_save_dir (str): The directory where the knowledge graph will be saved.

        Returns:
            str: The path to the saved knowledge graph image.

        Raises:
            FileNotFoundError: If the specified JSON file does not exist.
        """
        # Clean up file path and save directory inputs
        parsed_tables = parsed_tables.strip('"')
        path_to_save_dir = path_to_save_dir.strip('"')
        print(f"KnowledgeGraphBuilder received cleaned file path: {parsed_tables}")
        print(f"KnowledgeGraphBuilder received cleaned save directory: {path_to_save_dir}")

        # Check if file exists
        if not os.path.exists(parsed_tables):
            print(f"DEBUG: os.path.exists({parsed_tables}) -> {os.path.exists(parsed_tables)}")
            raise FileNotFoundError(f"File {parsed_tables} not found.")
        
        # Check if save directory exists, create if it does not
        if not os.path.exists(path_to_save_dir):
            os.makedirs(path_to_save_dir)

        # Tokenize the user query and remove stopwords
        tokens = word_tokenize(user_query.lower())
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]

        # Find the most frequent keyword
        freq_dist = nltk.FreqDist(tokens)
        top_keyword = freq_dist.max() if freq_dist else ""
        print(f"Top keyword from user query: {top_keyword}")

        # Load the JSON data
        with open(parsed_tables, 'r') as file:
            data = json.load(file)

        # Create a directed graph
        G = nx.DiGraph()

        # Populate the graph with nodes and edges
        for table_name, table_data in data.items():
            headers = table_data.get("headers", [])
            rows = table_data.get("rows", [])
            for row in rows:
                for i, item in enumerate(row):
                    header = headers[i] if i < len(headers) else f"Header_{i}"
                    G.add_node(item)
                    G.add_edge(header, item)
        
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
