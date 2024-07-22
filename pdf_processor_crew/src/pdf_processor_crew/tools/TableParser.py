from langchain.tools import tool
import pandas as pd
import json
import os
from typing import ClassVar

class TableParser:
    ParseTable: ClassVar

    @tool("parse_row_col")
    @staticmethod
    def ParseTable(save_dir: str, json_save_dir: str) -> str:
        """
        Parse rows and columns in CSV files in the save_dir directory and save the parsed results to a single JSON file.

        Args:
            save_dir (str): The directory containing the CSV files to be processed.
            json_save_dir (str): The directory where the parsed results will be saved.

        Returns:
            str: The path to the saved JSON file containing the parsed data.

        Raises:
            FileNotFoundError: If any of the specified CSV files does not exist.
        """
        # Clean up save directory input
        save_dir = save_dir.strip('"')
        json_save_dir = json_save_dir.strip('"')
        print(f"TableParser received cleaned save directory: {json_save_dir}")

        # Check if save directory exists, create if it does not
        if not os.path.exists(json_save_dir):
            os.makedirs(json_save_dir)
        
        parsed_data = {}

        for filename in os.listdir(save_dir):
            if filename.startswith("table_") and filename.endswith(".csv"):
                csv_path = os.path.join(save_dir, filename)
                
                # Check if file exists
                if not os.path.exists(csv_path):
                    print(f"DEBUG: os.path.exists({csv_path}) -> {os.path.exists(csv_path)}")
                    continue  # Skip non-existing files

                print(f"TableParser received cleaned file path: {csv_path}")

                # Load the CSV file
                df = pd.read_csv(csv_path)

                # Replace NaN values with None
                df = df.where(pd.notnull(df), None)
                rows = df.values.tolist()

                # Parse rows and columns
                headers = df.columns.tolist()  # Use columns as headers
                rows = rows  # All row data

                # Use the file name without extension as the table name
                table_name = os.path.splitext(filename)[0]

                parsed_data[table_name] = {
                    "headers": headers,  # Header information
                    "columns": list(df.columns),  # Original column names
                    "rows": rows  # Row data
                }

        # Save all parsed data to a single JSON file
        json_file_path = os.path.join(json_save_dir, 'all_parsed_tables.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(parsed_data, json_file, indent=4)
        
        print(f"All parsed data saved to: {json_file_path}")

        return json_file_path
