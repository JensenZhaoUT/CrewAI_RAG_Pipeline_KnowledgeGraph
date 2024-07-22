from langchain.tools import tool
from langchain_openai import ChatOpenAI
from .InformationRetriever import InformationRetriever
from typing import ClassVar, List, Dict
import json

class ResponseGenerator:
    GenerateResponse: ClassVar

    def __init__(self):
        self.llm = ChatOpenAI(
            model="crewai-llama3",
            base_url="http://localhost:11434/v1",
            api_key="NA"
        )

    @staticmethod
    @tool("generate_response")
    def GenerateResponse(user_query: str, json_file_path: str) -> str:
        """
        Generate a response to the user's query using the retrieved information.

        Args:
            user_query (str): The user's query.
            json_file_path (str): The path to the JSON file containing the parsed data.

        Returns:
            str: The generated response.
        """
        # Retrieve information using InformationRetriever
        try:
            retrieved_file_path = InformationRetriever.RetrieveInformation(user_query, json_file_path)
            with open(retrieved_file_path, 'r') as file:
                retrieved_info = json.load(file)
        except Exception as e:
            return f"Error retrieving information: {e}"

        # Create a prompt with the retrieved information and user query
        context = "Based on the retrieved information, answer the following query:\n"
        for info in retrieved_info:
            table_name = info["table_name"]
            header = info["header"]
            row = info["row"]
            context += f"Table: {table_name}\nHeader: {header}\nRow: {row}\n\n"
        
        context += f"User Query: {user_query}\n"
        
        # Generate a response using the LLM model
        try:
            response_generator = ResponseGenerator()
            response = response_generator.llm.predict(context)
        except Exception as e:
            return f"Error generating response: {e}"
        
        print(f"Generated response: {response}")

        return response, "RAG integration task completed."
