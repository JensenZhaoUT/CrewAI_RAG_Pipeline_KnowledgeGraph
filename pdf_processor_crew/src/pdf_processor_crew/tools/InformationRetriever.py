from rank_bm25 import BM25Okapi
import json
import os
from typing import List, Dict, ClassVar
from langchain.tools import tool

class InformationRetriever:
    RetrieveInformation: ClassVar

    @staticmethod
    @tool("retrieve_information")
    def RetrieveInformation(user_query: str, json_file_path: str) -> str:
        """
        Retrieve relevant information from the JSON files based on the user query using BM25 and save the results.

        Args:
            user_query (str): The user's query.
            json_file_path (str): The path to the JSON file containing the parsed data.

        Returns:
            str: Path to the saved results.
        """
        # Load the JSON data
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"JSON file {json_file_path} not found.")
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # Index the data for BM25 search
        contexts = []
        table_info = []
        for table_name, table_data in data.items():
            headers = table_data.get("headers", [])
            rows = table_data.get("rows", [])
            for row in rows:
                context = " ".join(row)
                contexts.append(context)
                table_info.append((table_name, headers, row))
        
        # Initialize BM25
        bm25 = BM25Okapi([context.split() for context in contexts])
        
        # Perform BM25 search
        query_terms = user_query.split()
        scores = bm25.get_scores(query_terms)
        
        # Retrieve top results
        top_n = 5
        top_indices = scores.argsort()[-top_n:][::-1]
        results = []
        for idx in top_indices:
            table_name, headers, row = table_info[idx]
            results.append({
                "table_name": table_name,
                "header": headers,
                "row": row
            })
        
        # Save the results
        save_dir = os.path.dirname(json_file_path)
        save_path = os.path.join(save_dir, "retrieved_results.json")
        with open(save_path, 'w') as file:
            json.dump(results, file, indent=4)
        
        print(f"Retrieved information saved to: {save_path}")

        return save_path
