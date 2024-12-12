import statistics
from typing import List, Dict, Any

from dataclasses import dataclass
from typing import Dict, List, Union, Any, Tuple
import statistics

@dataclass
class Descriptor:
    """Class for summarizing real estate data."""
    data: List[Dict[str, Any]]

    def none_ratio(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """
        Compute the ratio of None values per column.
        """
        if not self.data:
            raise ValueError("The dataset is empty!")
        
        columns_to_check = self._get_columns_to_check(columns)
        ratios = {}
        total_rows = len(self.data)

        for col in columns_to_check:
            none_count = sum(1 for row in self.data if row.get(col) is None)
            ratios[col] = none_count / total_rows
        return ratios

    def average(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """
        Compute the average value for numeric columns, ignoring None values.
        """
        columns_to_check = self._get_columns_to_check(columns, numeric_only=True)
        averages = {}

        for col in columns_to_check:
            values = [float(row[col]) for row in self.data if row.get(col) is not None]
            if values:
                averages[col] = sum(values) / len(values)
        return averages

    def median(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """
        Compute the median value for numeric columns, ignoring None values.
        """
        columns_to_check = self._get_columns_to_check(columns, numeric_only=True)
        medians = {}

        for col in columns_to_check:
            values = [float(row[col]) for row in self.data if row.get(col) is not None]
            if values:
                medians[col] = statistics.median(values)
        return medians

    def percentile(self, columns: Union[List[str], str] = "all", percentile: int = 50) -> Dict[str, float]:
        """
        Compute the specified percentile for numeric columns, ignoring None values.
        """
        columns_to_check = self._get_columns_to_check(columns, numeric_only=True)
        percentiles = {}

        for col in columns_to_check:
            values = [float(row[col]) for row in self.data if row.get(col) is not None]
            if values:
                values.sort()
                index = int(len(values) * (percentile / 100))
                percentiles[col] = values[min(index, len(values) - 1)]
        return percentiles

    def type_and_mode(self, columns: Union[List[str], str] = "all") -> Dict[str, Tuple[str, Union[str, float]]]:
        """
        Determine the type and mode of the columns.
        """
        columns_to_check = self._get_columns_to_check(columns)
        types_and_modes = {}

        for col in columns_to_check:
            non_none_values = [row[col] for row in self.data if row.get(col) is not None]
            if non_none_values:
                # Infer type and calculate mode
                value_type = type(non_none_values[0]).__name__
                mode_value = statistics.mode(non_none_values)
                types_and_modes[col] = (value_type, mode_value)
            else:
                types_and_modes[col] = ("None", None)
        return types_and_modes

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Union, Any, Tuple

@dataclass
class DescriptorNumpy:
    """Class for summarizing real estate data using NumPy."""
    data: List[Dict[str, Any]]

    def __post_init__(self):
        """
        Convert the list of dictionaries into a NumPy-friendly format upon initialization.
        """
        if not self.data:
            raise ValueError("The dataset is empty!")

        # Extract all keys (columns) and prepare a structured NumPy array
        self.columns = list(self.data[0].keys())
        self.array = np.array([
            [row.get(col, None) for col in self.columns]
            for row in self.data
        ], dtype=object)

    def none_ratio(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """
        Compute the ratio of None values per column.
        """
        columns_to_check = self._get_columns_to_check(columns)
        ratios = {}

        for col in columns_to_check:
            col_idx = self.columns.index(col)
            none_count = np.sum(self.array[:, col_idx] == None)  # Count None values
            ratios[col] = none_count / len(self.array)
        return ratios

    def average(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """
        Compute the average for numeric columns, ignoring None values.
        """
        columns_to_check = self._get_columns_to_check(columns, numeric_only=True)
        averages = {}

        for col in columns_to_check:
            col_idx = self.columns.index(col)
            numeric_values = self._get_numeric_column(col_idx)
            if numeric_values.size > 0:
                averages[col] = np.mean(numeric_values)
        return averages

    def median(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """
        Compute the median for numeric columns, ignoring None values.
        """
        columns_to_check = self._get_columns_to_check(columns, numeric_only=True)
        medians = {}

        for col in columns_to_check:
            col_idx = self.columns.index(col)
            numeric_values = self._get_numeric_column(col_idx)
            if numeric_values.size > 0:
                medians[col] = np.median(numeric_values)
        return medians

    def _get_columns_to_check(self, columns: Union[List[str], str], numeric_only: bool = False) -> List[str]:
        """
        Helper function to determine which columns to process.
        """
        if columns == "all":
            if numeric_only:
                return [col for col in self.columns if self._is_numeric_column(col)]
            return self.columns

        # Validate provided columns
        for col in columns:
            if col not in self.columns:
                raise ValueError(f"Column '{col}' not found in data.")
        
        if numeric_only:
            return [col for col in columns if self._is_numeric_column(col)]
        return columns

    def _is_numeric_column(self, column: str) -> bool:
        """Check if a column contains numeric data."""
        col_idx = self.columns.index(column)
        column_values = self.array[:, col_idx]
        return all(self._is_numeric(value) for value in column_values if value is not None)

    def _get_numeric_column(self, col_idx: int) -> np.ndarray:
        """
        Get numeric values from a specific column, ignoring None values.
        """
        column_values = self.array[:, col_idx]
        numeric_values = [float(value) for value in column_values if self._is_numeric(value)]
        return np.array(numeric_values)

    def _is_numeric(self, value: Any) -> bool:
        """Check if a value is numeric."""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

