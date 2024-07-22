from langchain.tools import tool
import json
import os
from typing import ClassVar, List, Dict

class InformationRetriever:
    RetrieveInformation: ClassVar

    @staticmethod
    @tool("retrieve_information")
    def RetrieveInformation(user_query: str, json_file_path: str) -> List[Dict]:
        """
        Retrieve relevant information from the JSON files based on the user query.

        Args:
            user_query (str): The user's query.
            json_file_path (str): The path to the JSON file containing the parsed data.

        Returns:
            List[Dict]: Retrieved information relevant to the user query.
        """
        # Load the JSON data
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"JSON file {json_file_path} not found.")
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # Index the data for efficient search
        index = {}
        for table_name, table_data in data.items():
            headers = table_data.get("headers", [])
            rows = table_data.get("rows", [])
            for row in rows:
                for header, cell in zip(headers, row):
                    if cell is not None:
                        index.setdefault(cell.lower(), []).append((table_name, header, row))
        
        # Search the index for the query
        query = user_query.lower()
        results = []
        if query in index:
            entries = index[query]
            for table_name, header, row in entries:
                results.append({
                    "table_name": table_name,
                    "header": header,
                    "row": row
                })

        print(f"Retrieved information: {results}")

        return results
