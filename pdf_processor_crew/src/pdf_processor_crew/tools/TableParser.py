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

        def split_and_combine_transpose(data):
            # Insert 'null\nnull\nnull' to index 4, 5, and 6
            data[4] = 'null\n' + data[4]
            data[5] = 'null\n' + data[5]
            data[6] = 'null\n' + data[6]

            split_data = [item.split('\n') for item in data[:-2]]  # Split all except the last two items
            last_two_items = data[-2:]  # Get the last two items
            transposed_data = list(map(list, zip(*split_data)))  # Transpose the split lists
            combined_data = [sublist + last_two_items for sublist in transposed_data]  # Combine transposed lists with the last two items
            return combined_data

        # Process general tables
        for i in range(1, 37):  # Iterate through general tables (1-35)
            csv_path = os.path.join(save_dir, f"table_{i-1}.csv")
            
            # Check if file exists
            if not os.path.exists(csv_path):
                print(f"DEBUG: os.path.exists({csv_path}) -> {os.path.exists(csv_path)}")
                continue  # Skip non-existing files

            print(f"TableParser received cleaned file path: {csv_path}")

            # Load the CSV file
            df = pd.read_csv(csv_path)

            # Replace NaN values with "null"
            df = df.fillna("null")
            rows = df.values.tolist()

            headers = rows[0] if rows else []
            rows = rows[1:]  # Exclude the header row from rows

            parsed_data[f"table_{i-1}"] = {
                "headers": headers,  # Header information
                "columns": list(df.columns),  # Original column names
                "rows": rows  # Row data
            }
        special_headers = [
            "Field Number",
            "Identifier",
            "Field Name",
            "Character",
            "Field Size Min",
            "Field Size Max",
            "Occurrences Min",
            "Occurrences Max",
            "Example",
            "Comments/Special Characters"
        ]

        # Process special tables (36-41)
        for i in range(37, 43):  # Iterate through special tables (36-41)
            csv_path = os.path.join(save_dir, f"table_{i-1}.csv")
            
            # Check if file exists
            if not os.path.exists(csv_path):
                print(f"DEBUG: os.path.exists({csv_path}) -> {os.path.exists(csv_path)}")
                continue  # Skip non-existing files

            print(f"TableParser received cleaned file path: {csv_path}")

            # Load the CSV file
            df = pd.read_csv(csv_path)

            # Replace NaN values with "null"
            df = df.fillna("null")
            rows = df.values.tolist()

            processed_rows = [rows[0]]  # Keep the header row as is
            for row in rows[1:]:  # Skip the first row (header)
                if '\n' in row[0]:
                    processed_rows.extend(split_and_combine_transpose(row))
                else:
                    processed_rows.append(row)

            headers = special_headers
            rows = processed_rows[1:]  # Exclude the header row from rows

            parsed_data[f"table_{i-1}"] = {
                "headers": headers,  # Header information
                "columns": list(df.columns),  # Original column names
                "rows": rows  # Row data
            }
                    # Process special tables (36-41)

        # Process remaining tables
        for i in range(43, 53):  # Iterate through remaining tables (42-60)
            csv_path = os.path.join(save_dir, f"table_{i-1}.csv")
            
            # Check if file exists
            if not os.path.exists(csv_path):
                # print(f"DEBUG: os.path.exists({csv_path}) -> {os.path.exists(csv_path)}")
                continue  # Skip non-existing files

            print(f"TableParser received cleaned file path: {csv_path}")

            # Load the CSV file
            df = pd.read_csv(csv_path)

            # Replace NaN values with "null"
            df = df.fillna("null")
            rows = df.values.tolist()

            headers = rows[0] if rows else []
            rows = rows[1:]  # Exclude the header row from rows

            parsed_data[f"table_{i-1}"] = {
                "headers": headers,  # Header information
                "columns": list(df.columns),  # Original column names
                "rows": rows  # Row data
            }

        # Save all parsed data to a single JSON file
        json_file_path = os.path.join(json_save_dir, 'all_parsed_tables.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(parsed_data, json_file, indent=4)
        
        print(f"All parsed data saved to: {json_file_path}")

        return json_file_path, "Table parsing task completed."
