from dataclasses import dataclass
from typing import Dict, List, Any
import re

@dataclass
class Cleaner:
    """Class for cleaning real estate data."""
    data: List[Dict[str, Any]]

    def rename_with_best_practices(self) -> None:
        """
        Rename the columns with snake_case naming convention.
        """
        if not self.data:
            raise ValueError("The dataset is empty!")

        # Rename the keys in the first row using snake_case
        old_keys = list(self.data[0].keys())
        new_keys = [self._to_snake_case(key) for key in old_keys]

        # Replace all row keys with snake_case keys
        for row in self.data:
            for old_key, new_key in zip(old_keys, new_keys):
                row[new_key] = row.pop(old_key)

    def _to_snake_case(self, name: str) -> str:
        """
        Convert a string to snake_case.
        """
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        name = re.sub(r'[\s\-]+', '_', name)  # Replace spaces and hyphens
        return name

    def na_to_none(self) -> List[Dict[str, Any]]:
        """
        Replace 'NA' values with Python's None.
        
        Returns:
            The cleaned dataset.
        """
        for row in self.data:
            for key, value in row.items():
                if value == "NA":
                    row[key] = None
        return self.data
