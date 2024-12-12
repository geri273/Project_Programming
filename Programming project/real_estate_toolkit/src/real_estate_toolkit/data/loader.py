from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any
import csv

@dataclass
class DataLoader:
    """Class for loading and basic processing of real estate data."""
    data_path: Path

    def load_data_from_csv(self) -> List[Dict[str, Any]]:
        """
        Load data from a CSV file into a list of dictionaries.

        Returns:
            A list of dictionaries where each row is represented as a dictionary.
        """
        data = []
        try:
            with self.data_path.open(mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convert "NA" to None for missing values
                    clean_row = {key: (value if value != "NA" else None) for key, value in row.items()}
                    data.append(clean_row)
        except FileNotFoundError as e:
            print(f"Error: File not found at {self.data_path}")
            raise e
        return data

    def validate_columns(self, required_columns: List[str]) -> bool:
        """
        Validate that all required columns are present in the dataset.

        Args:
            required_columns (List[str]): List of required column names.

        Returns:
            True if all required columns are present, otherwise False.
        """
        sample_data = self.load_data_from_csv()
        if not sample_data:
            raise ValueError("The dataset is empty!")
        
        actual_columns = sample_data[0].keys()
        missing_columns = [col for col in required_columns if col not in actual_columns]
        
        if missing_columns:
            print(f"Missing columns: {missing_columns}")
            return False
        return True
