import re
from typing import List, Dict, Any

class Cleaner: 

    def __init__(self, data: list):
        """
        Initialize the Cleaner with data.

        Args:
            data (list): The dataset to clean, represented as a list of dictionaries.
        """
        self.data = data
    
    def __getitem__(self, index):
        return self.data[index]
        
    def rename_with_best_practices(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not data:
            return data
        
        columns = data[0].keys()
        renamed_columns = {}

        for col in columns:
            new_col_name = re.sub(r'[^a-zA-Z0-9]', '_', col).lower()
            renamed_columns[col] = new_col_name

        for row in data:
            for old_col, new_col in renamed_columns.items():
                if old_col in row:
                    row[new_col] = row.pop(old_col)

        return data

    def na_to_none(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for row in data:
            for key, value in row.items():
                if value == 'NA':
                    row[key] = None
        return data

    def getitem(self, index):
        """
        Allow Cleaner object to be accessed like a list.
        """
        return self.data[index]
    def __len__(self):
        """
        Return the length of the cleaned dataset.
        """
        return len(self.data)
