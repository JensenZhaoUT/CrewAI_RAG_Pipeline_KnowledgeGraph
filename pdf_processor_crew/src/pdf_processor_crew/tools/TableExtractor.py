from langchain.tools import tool
import camelot
import pandas as pd
import os
from typing import ClassVar

class TableExtractor:
    ExtractTables: ClassVar

    @tool("extract_tables_from_pdf")
    @staticmethod
    def ExtractTables(pdf_path: str, save_dir: str) -> list:
        """
        Extract tables from the PDF file in the pdf_path and save them as preprocessed CSV files.

        Args:
            pdf_path (str): The path to the PDF file to be processed.
            save_dir (str): The directory where the extracted tables will be saved.

        Returns:
            list: A list of paths to the saved preprocessed CSV files.

        Raises:
            FileNotFoundError: If the specified PDF file does not exist.
        """
        # Clean up file path and save directory inputs
        pdf_path = pdf_path.strip('"')
        save_dir = save_dir.strip('"')
        print(f"TableExtractor received cleaned file path: {pdf_path}")
        print(f"TableExtractor received cleaned save directory: {save_dir}")

        # Check if file exists
        if not os.path.exists(pdf_path):
            print(f"DEBUG: os.path.exists({pdf_path}) -> {os.path.exists(pdf_path)}")
            raise FileNotFoundError(f"File {pdf_path} not found.")
        
        # Check if save directory exists, create if it does not
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Use Camelot to extract tables from the PDF file
        tables = camelot.read_pdf(pdf_path, pages='all')
        table_paths = []

        # Save each extracted table as a preprocessed CSV file
        for i, table in enumerate(tables):
            # Convert the table to a DataFrame
            df = table.df

            # Preprocessing: Remove empty rows and columns
            df = df.dropna(how='all', axis=0)
            df = df.dropna(how='all', axis=1)

            # Convert all data to string type
            df = df.astype(str)

            # Save preprocessed table to a CSV file
            csv_file_path = os.path.join(save_dir, f"table_{i}.csv")
            df.to_csv(csv_file_path, index=False)
            table_paths.append(csv_file_path)
        
        print(f"Extracted and preprocessed tables saved to: {table_paths}")

        return "Document ingestion tasks completed."