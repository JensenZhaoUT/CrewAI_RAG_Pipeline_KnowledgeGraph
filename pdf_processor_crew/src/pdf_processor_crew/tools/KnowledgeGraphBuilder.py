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
        
        # Initialize the parsed_result dictionary
        parsed_result = {}

        # Search for the keyword in the rows of the tables
        for table_name, table_data in data.items():
            headers = table_data.get("headers", [])
            rows = table_data.get("rows", [])
            for row in rows:
                if len(row) > 1 and row[1].lower() == top_keyword.lower():
                    parsed_result[table_name] = {
                        "headers": headers,
                        "row": row
                    }
                    break  # Stop searching once a match is found
        
        print(f"Parsed result: {parsed_result}")

        # Create a directed graph
        G = nx.DiGraph()

        # Add the top_keyword as the central node
        G.add_node(top_keyword)

        # Populate the graph with nodes and edges from parsed_result
        for table_name, table_data in parsed_result.items():
            headers = table_data.get("headers", [])
            row = table_data.get("row", [])
            for i, item in enumerate(row):
                header = headers[i] if i < len(headers) else f"Header_{i}"
                G.add_node(item)
                G.add_edge(top_keyword, item, label=header)
        
        # Define the save path for the knowledge graph image
        graph_image_path = os.path.join(path_to_save_dir, "knowledge_graph_2.png")
        
        # Draw the graph
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_shape='s', node_size=3000)
        nx.draw_networkx_nodes(G, pos, nodelist=[top_keyword], node_color='lightgreen', node_shape='o', node_size=5000)

        # Draw edges
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['label'] for u, v, d in G.edges(data=True)})

        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

        plt.title("Knowledge Graph")
        plt.axis('off')
        plt.show()
        plt.savefig(graph_image_path)

        print(f"Knowledge graph saved to: {graph_image_path}")

        return graph_image_path
