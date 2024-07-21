from langchain.tools import tool
import json
import os
from typing import ClassVar

class InformationRetriever:
    RetrieveInformation: ClassVar

    @tool("retrieve_information")
    @staticmethod
    def RetrieveInformation(user_query: str, json_file_path: str) -> dict:
        """
        Retrieve relevant information from the JSON files based on the user query.

        Args:
            user_query (str): The user's query.
            json_file_path (str): The directory containing the parsed JSON files.

        Returns:
            dict: Retrieved information relevant to the user query.
        """
        # Load the JSON files
        retrieved_info = []
        for json_file in os.listdir(json_file_path):
            if json_file.endswith('.json'):
                with open(os.path.join(json_file_path, json_file), 'r') as f:
                    data = json.load(f)
                    # Here you can add more sophisticated query-based retrieval logic
                    if user_query.lower() in json.dumps(data).lower():
                        retrieved_info.append(data)
        
        print(f"Retrieved information: {retrieved_info}")

        return retrieved_info
