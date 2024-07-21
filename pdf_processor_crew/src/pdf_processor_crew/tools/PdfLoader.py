from crewai_tools import BaseTool
from langchain.tools import tool
import fitz  # PyMuPDF
import os
from typing import ClassVar

class PDFLoader(BaseTool):
    LoadPdf: ClassVar

    @tool("load_and_pdf_file")
    @staticmethod
    def LoadPdf(file_path: str, save_dir: str) -> str:
        """
        Load and read a PDF file from the given file path and save the extracted text to a .txt file.

        Args:
            file_path (str): The path to the PDF file to be loaded.
            save_dir (str): The directory where the extracted text file will be saved.

        Returns:
            str: The path to the saved text file.

        Raises:
            FileNotFoundError: If the specified PDF file does not exist.
        """
        # Clean up file path and save directory inputs
        file_path = file_path.strip('"')
        save_dir = save_dir.strip('"')
        print(f"PDFLoader received cleaned file path: {file_path}")
        print(f"PDFLoader received cleaned save directory: {save_dir}")

        # Check if file exists
        if not os.path.exists(file_path):
            print(f"DEBUG: os.path.exists({file_path}) -> {os.path.exists(file_path)}")
            raise FileNotFoundError(f"File {file_path} not found.")
        
        # Check if save directory exists, create if it does not
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Load PDF file using PyMuPDF
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()

        # Define the path for the output text file
        txt_file_path = os.path.join(save_dir, os.path.basename(file_path).replace('.pdf', '.txt'))

        # Save the extracted text to a .txt file
        with open(txt_file_path, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"Extracted text saved to: {txt_file_path}")

        return txt_file_path
