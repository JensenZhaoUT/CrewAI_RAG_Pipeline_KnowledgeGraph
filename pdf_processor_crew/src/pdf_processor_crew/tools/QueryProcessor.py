from langchain.tools import tool
from concurrent.futures import ThreadPoolExecutor
import json
from typing import ClassVar
from .InformationRetriever import InformationRetriever
from .ResponseGenerator import ResponseGenerator
class QueryProcessor:
    ProcessQueries: ClassVar

    @tool("process_queries")
    @staticmethod
    def ProcessQueries(queries: list, json_file_path: str) -> list:
        """
        Process multiple user queries in parallel.

        Args:
            queries (list): A list of user queries.
            json_file_path (str): The directory containing the parsed JSON files.

        Returns:
            list: A list of responses to the user queries.
        """
        def process_query(query):
            retrieved_info = InformationRetriever.RetrieveInformation(query, json_file_path)
            return ResponseGenerator.GenerateResponse(retrieved_info, query)

        with ThreadPoolExecutor() as executor:
            responses = list(executor.map(process_query, queries))
        
        print(f"Processed queries: {responses}")

        return responses
