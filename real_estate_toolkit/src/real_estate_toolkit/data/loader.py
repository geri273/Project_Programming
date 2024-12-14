from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Union
import csv

class DataLoader: 

    data_path: Path

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = None
        
    def load_data_from_csv(self) -> List[Dict[str, float]]:

        data = []
        try:
            with self.data_path.open(mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except FileNotFoundError as e:
            print(f"Error: File not found at {self.data_path}")
            raise e
        return data
    
    def validate_columns(self, required_columns: List[str]) -> bool:
        sample_data = self.load_data_from_csv()
        if not sample_data:
            raise ValueError("The dataset is empty!")
        
        actual_columns = sample_data[0].keys()
        missing_columns = [col for col in required_columns if col not in actual_columns]
        
        if missing_columns:
            print(f"Missing columns: {missing_columns}")
            return False
        return True

