from langchain.tools import tool
from langchain_openai import ChatOpenAI
from .InformationRetriever import InformationRetriever
from typing import ClassVar, List, Dict
import json

class ResponseGenerator:
    GenerateResponse: ClassVar

    def __init__(self):
        self.llm = ChatOpenAI(
            model="crewai-llama3.1-8b",
            base_url="http://localhost:11434/v1",
            api_key="NA"
        )

    @staticmethod
    @tool("generate response")
    def GenerateResponse(user_query: str, text_file_path: str) -> str:
        """
        Generate a response to the user's query using the retrieved information.

        Args:
            user_query (str): The user's query.
            text_file_path (str): The path to the text file containing relevant information.

        Returns:
            str: The generated response.
        """
        # Retrieve information using InformationRetriever
        retrieved_info = InformationRetriever.RetrieveInformation(user_query, text_file_path)
        # print("The retrieved info is:", retrieved_info)

        # Create a prompt with the retrieved information and user query
        context = "Based on the retrieved information, answer the following query:\n"
        for info in retrieved_info:
            context += f"Relevant text: {info.get('context')}\n\n"
        
        context += f"User Query: {user_query}\n"
        
        # Instantiate ResponseGenerator to access the llm instance
        response_generator = ResponseGenerator()
        # Generate a response using the LLM model
        response = response_generator.llm.predict(context)
        
        print(f"Generated response: {response}")

        return response, "RAG integration task completed."
