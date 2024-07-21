from langchain.tools import tool
import json
import os
from typing import ClassVar

class PromptProcessor:
    HandlePrompt: ClassVar

    @tool("Handle user prompt")
    @staticmethod
    def HandlePrompt(query: str) -> str:
        """
        Parse rows and columns in CSV files in the save_dir directory and save the parsed results to JSON files.

        Args:
            save_dir (str): The directory containing the CSV files to be processed.
            json_save_dir (str): The directory where the parsed results will be saved.

        Returns:
            List[str]: A list of paths to the saved JSON files containing the parsed data.

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
        
        parsed_data_paths = []

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
            columns = list(df.columns)

            parsed_data = {
                "columns": columns,  # Header information
                "rows": rows         # Row data
            }

            # Save parsed data to a JSON file
            json_file_path = os.path.join(json_save_dir, os.path.basename(csv_path).replace('.csv', '_parsed.json'))
            with open(json_file_path, 'w') as json_file:
                json.dump(parsed_data, json_file, indent=4)
            
            parsed_data_paths.append(json_file_path)
            print(f"Parsed data saved to: {json_file_path}")

        return parsed_data_paths, "Table parsing task completed."