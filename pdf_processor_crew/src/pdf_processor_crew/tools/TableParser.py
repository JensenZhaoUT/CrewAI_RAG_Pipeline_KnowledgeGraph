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

        for i in range(1, 61):  # Iterate through potential CSV files (1-60)
            csv_path = os.path.join(save_dir, f"table_{i}.csv")
            
            # Check if file exists
            if not os.path.exists(csv_path):
                print(f"DEBUG: os.path.exists({csv_path}) -> {os.path.exists(csv_path)}")
                continue  # Skip non-existing files

            print(f"TableParser received cleaned file path: {csv_path}")

            # Load the CSV file
            df = pd.read_csv(csv_path)

            # Parse rows and columns
            rows = df.values.tolist()
            headers = rows[0] if rows else []
            rows = rows[1:]  # Exclude the header row from rows

            parsed_data[f"table_{i}"] = {
                "headers": headers,  # Header information
                "columns": list(df.columns),  # Original column names
                "rows": rows  # Row data
            }

        # Save all parsed data to a single JSON file
        json_file_path = os.path.join(json_save_dir, 'all_parsed_tables.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(parsed_data, json_file, indent=4)
        
        print(f"All parsed data saved to: {json_file_path}")

        return "Table parsing task completed."
