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
    def RetrieveInformation(user_query: str, text_file_path: str, json_file_path: str) -> List[Dict[str, str]]:
        """
        Retrieve relevant information from the text and JSON files based on the user query using BM25 and save the results.

        Args:
            user_query (str): The user's query.
            text_file_path (str): The path to the text file containing extracted text.
            json_file_path (str): The path to the JSON file containing parsed data.

        Returns:
            List[Dict[str, str]]: List of retrieved information with source and data.
        """

        text_file_path = text_file_path.strip('"')
        json_file_path = json_file_path.strip('"')

        results = []
        
        # Load and process the text file
        text_data = []
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r') as file:
                text_data = file.read().split('\n')
            # Index the text data for BM25 search
            bm25_text = BM25Okapi([line.split() for line in text_data])
            text_scores = bm25_text.get_scores(user_query.split())
            top_text_indices = text_scores.argsort()[-5:][::-1]
            for idx in top_text_indices:
                results.append({"source": "text", "data": text_data[idx]})
        else:
            print(f"Text file not found: {text_file_path}")

        # Debugging information
        print(f"Text data: {text_data}")
        print(f"BM25 text scores: {text_scores}")
        print(f"Top text indices: {top_text_indices}")

        # Load and process the JSON file
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)
            # Index the JSON data for BM25 search
            contexts = []
            table_info = []
            for table_name, table_data in json_data.items():
                headers = table_data.get("headers", [])
                rows = table_data.get("rows", [])
                for row in rows:
                    context = " ".join(row)
                    contexts.append(context)
                    table_info.append((table_name, headers, row))
            bm25_json = BM25Okapi([context.split() for context in contexts])
            json_scores = bm25_json.get_scores(user_query.split())
            top_json_indices = json_scores.argsort()[-5:][::-1]
            for idx in top_json_indices:
                table_name, headers, row = table_info[idx]
                results.append({"source": f"table {table_name}", "data": f"Headers: {headers}, Row: {row}"})
        else:
            print(f"JSON file not found: {json_file_path}")

        # Debugging information
        print(f"JSON data: {json_data}")
        print(f"BM25 JSON contexts: {contexts}")
        print(f"BM25 JSON scores: {json_scores}")
        print(f"Top JSON indices: {top_json_indices}")

        print(f"Retrieved information: {results}")

        return results

    def invoke(self, *args):
        return self.RetrieveInformation(*args)
