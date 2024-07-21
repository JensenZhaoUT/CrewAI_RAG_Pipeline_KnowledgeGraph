from langchain.tools import tool
import json
from typing import ClassVar

class ResponseGenerator:
    GenerateResponse: ClassVar

    @tool("generate_response")
    @staticmethod
    def GenerateResponse(retrieved_info: dict, user_query: str) -> str:
        """
        Generate a response to the user query based on the retrieved information.

        Args:
            retrieved_info (dict): The information retrieved from the JSON files.
            user_query (str): The user's query.

        Returns:
            str: The generated response.
        """
        # Here you can use a language model to generate a response based on the retrieved information
        response = f"Based on the retrieved information, here is the answer to your query '{user_query}':\n{json.dumps(retrieved_info, indent=4)}"
        
        print(f"Generated response: {response}")

        return response
