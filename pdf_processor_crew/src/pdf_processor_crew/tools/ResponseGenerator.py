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

    def generate_response(self, context: str) -> str:
        """
        Generate a response using the LLM model.

        Args:
            context (str): The context for the LLM to generate a response.

        Returns:
            str: The generated response.
        """
        try:
            response = self.llm.predict(context)
        except Exception as e:
            return f"Error generating response: {e}"

        print(f"Generated response: {response}")

        return response

    @staticmethod
    @tool("generate_response")
    def GenerateResponse(user_query: str, text_file_path: str, json_file_path: str) -> str:
        """
        Generate a response to the user's query using the retrieved information from both text and JSON files.

        Args:
            user_query (str): The user's query.
            text_file_path (str): The path to the text file containing extracted text.
            json_file_path (str): The path to the JSON file containing parsed data.

        Returns:
            str: The generated response.
        """
        # Retrieve information using InformationRetriever
        try:
            information_retriever = InformationRetriever()
            retrieved_info = information_retriever.invoke(user_query, text_file_path, json_file_path)
            print(f"Retrieved information: {retrieved_info}")
        except Exception as e:
            return f"Error retrieving information: {e}"

        # Create a prompt with the retrieved information and user query
        context = "Based on the retrieved information, answer the following query:\n"
        for info in retrieved_info:
            source = info["source"]
            data = info["data"]
            context += f"Source: {source}\nData: {data}\n\n"
        
        context += f"User Query: {user_query}\n"
        
        # Generate a response using the LLM model
        try:
            response_generator = ResponseGenerator()
            response = response_generator.generate_response(context)
        except Exception as e:
            return f"Error generating response: {e}"
        
        return response
