from langchain.tools import tool
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from typing import ClassVar

nltk.download('stopwords')
nltk.download('wordnet')

class PromptProcessor:
    HandlePrompt: ClassVar

    @tool("handle_prompt")
    @staticmethod
    def HandlePrompt(user_query: str) -> str:
        """
        Process the user's query using NLP techniques to refine and prepare it for efficient information retrieval.

        Args:
            user_query (str): The user's query to be processed.

        Returns:
            str: The processed user query.
        """
        # Lowercase the query
        user_query = user_query.lower()

        # Remove special characters and digits
        user_query = re.sub(r'[^a-zA-Z\s]', '', user_query)

        # Tokenize the query
        tokens = user_query.split()

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]

        # Lemmatize the tokens
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]

        # Join tokens back into a string
        processed_query = ' '.join(tokens)
        
        print(f"Processed query: {processed_query}")

        return processed_query, "User prompt processed."
