from langchain.tools import tool
from langchain_openai import ChatOpenAI
from typing import ClassVar, List, Dict
from .InformationRetriever import InformationRetriever

class ResponseGenerator:
    GenerateResponse: ClassVar

    def __init__(self):
        self.llm = ChatOpenAI(
            model="crewai-llama3",
            base_url="http://localhost:11434/v1",
            api_key="NA"
        )
        self.info_retriever = InformationRetriever()  # Instantiate the InformationRetriever

    @tool("generate_response")
    @staticmethod
    def GenerateResponse(user_query: str, json_file_path: str) -> str:
        """
        Generate a response to the user's query using the retrieved information.

        Args:
            user_query (str): The user's query.
            json_file_path (str): The directory containing the parsed JSON files.

        Returns:
            str: The generated response.
        """
        # Retrieve information using the InformationRetriever tool
        retrieved_info = InformationRetriever.RetrieveInformation(user_query, json_file_path)

        # Create a prompt with the retrieved information and user query
        context = "Based on the retrieved information, answer the following query:\n"
        for info in retrieved_info:
            table_name = info.get("table_name", "N/A")
            header = info.get("header", "N/A")
            row = info.get("row", "N/A")
            context += f"Table: {table_name}\nHeader: {header}\nRow: {row}\n\n"
        
        context += f"User Query: {user_query}\n"
        
        # Generate a response using the LLM model
        response = ResponseGenerator().llm.predict(context)
        
        print(f"Generated response: {response}")

        return response
