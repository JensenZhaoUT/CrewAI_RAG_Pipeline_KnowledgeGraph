from langchain.tools import tool
import camelot
import pandas as pd
import os
from typing import ClassVar, Dict, List

class TableExtractor:
    ExtractTables: ClassVar

    @tool("extract_tables_from_pdf")
    @staticmethod
    def ExtractTables(pdf_path: str, save_dir: str) -> List[Dict[str, str]]:
        """
        Extract tables from the PDF file in the pdf_path and save them as preprocessed CSV files.

        Args:
            pdf_path (str): The path to the PDF file to be processed.
            save_dir (str): The directory where the extracted tables will be saved.

        Returns:
            list: A list of dictionaries containing paths to the saved preprocessed CSV files and their associated titles.

        Raises:
            FileNotFoundError: If the specified PDF file does not exist.
        """
        pdf_path = pdf_path.strip('"')
        save_dir = save_dir.strip('"')
        print(f"TableExtractor received cleaned file path: {pdf_path}")
        print(f"TableExtractor received cleaned save directory: {save_dir}")

        if not os.path.exists(pdf_path):
            print(f"DEBUG: os.path.exists({pdf_path}) -> {os.path.exists(pdf_path)}")
            raise FileNotFoundError(f"File {pdf_path} not found.")
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')
        table_paths = []

        for i, table in enumerate(tables):
            df = table.df

            df = df.dropna(how='all', axis=0)
            df = df.dropna(how='all', axis=1)

            df = df.astype(str)

            csv_file_path = os.path.join(save_dir, f"table_{i}.csv")
            df.to_csv(csv_file_path, index=False)

            # Capture the table title or metadata if available
            table_title = df.iloc[0, 0] if not df.empty else f"table_{i}"
            table_paths.append({"title": table_title, "path": csv_file_path})
        
        print(f"Extracted and preprocessed tables saved to: {table_paths}")

        return table_paths
