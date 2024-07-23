from rank_bm25 import BM25Okapi
import json
import os
from typing import List, Dict, ClassVar
from langchain.tools import tool

class InformationRetriever:
    RetrieveInformation: ClassVar

    def __init__(self):
        self.tool = tool("retrieve_information")(self.RetrieveInformation)

    @staticmethod
    def RetrieveInformation(user_query: str, text_file_path: str) -> List[Dict[str, str]]:
        """
        Retrieve relevant information from the text and JSON files based on the user query using BM25.

        Args:
            user_query (str): The user's query.
            text_file_path (str): The path to the text file containing extracted text.
            json_file_path (str): The path to the JSON file containing parsed data.

        Returns:
            List[Dict[str, str]]: List of retrieved information with source and data.
        """
        text_file_path = text_file_path.strip('"')
        # Check if the text file exists
        if not os.path.exists(text_file_path):
            raise FileNotFoundError(f"Text file {text_file_path} not found.")
        
        # Read the text file
        with open(text_file_path, 'r') as file:
            text_data = file.read()

        # Split the text data into sections for BM25 indexing
        text_contexts = text_data.split("\n\n")
        bm25 = BM25Okapi([context.split() for context in text_contexts])
        
        # Perform BM25 search
        query_terms = user_query.split()
        scores = bm25.get_scores(query_terms)
        
        # Retrieve top result
        top_index = scores.argsort()[-1:][::-1][0]  # Top 1 result
        retrieved_context = text_contexts[top_index]
        
        results = [{"context": retrieved_context}]

        print(f"Retrieved information: {results}")

        return results