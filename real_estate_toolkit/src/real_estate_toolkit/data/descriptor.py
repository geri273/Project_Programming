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
    import numpy as np
    from typing import List, Dict, Any

    def none_ratio(data: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate the ratio of None (missing) values for each column in the dataset using NumPy.
    
        Args:
        data: List of dictionaries representing rows in the dataset.
    
        Returns:
        A dictionary where keys are column names and values are the missing data ratio.
        """
        if not data:
            return {}

        # Convert data to numpy array for numerical operations
        columns = data[0].keys()
        column_data = {col: [] for col in columns}
    
        for row in data:
            for col in columns:
                column_data[col].append(row[col])

        # Convert each column to a numpy array and calculate the ratio of None values
        none_ratios = {}
        for col, values in column_data.items():
            arr = np.array(values, dtype=object)  # dtype=object to handle None values
            none_ratios[col] = np.sum(arr == None) / len(arr)  # Ratio of None values
    
        return none_ratios

    def average(data: List[Dict[str, Any]], column: str) -> float:
        """
        Calculate the average value for a numeric column in the dataset using NumPy.
    
        Args:
            data: List of dictionaries representing rows in the dataset.
            column: The column name for which to calculate the average.
    
        Returns:
            The average value of the column, or None if the column is empty or non-numeric.
        """
        values = [row[column] for row in data if row[column] is not None and isinstance(row[column], (int, float))]
        if not values:
            return None
        return np.mean(values)

    def median(data: List[Dict[str, Any]], column: str) -> float:
        """
        Calculate the median value for a numeric column in the dataset using NumPy.
    
        Args:
            data: List of dictionaries representing rows in the dataset.
            column: The column name for which to calculate the median.
    
        Returns:
            The median value of the column, or None if the column is empty or non-numeric.
        """
        values = [row[column] for row in data if row[column] is not None and isinstance(row[column], (int, float))]
        if not values:
            return None
        return np.median(values)

    def percentile(data: List[Dict[str, Any]], column: str, p: float = 90) -> float:
        """
        Calculate the nth percentile for a numeric column in the dataset using NumPy.
    
        Args:
            data: List of dictionaries representing rows in the dataset.
            column: The column name for which to calculate the percentile.
            p: The desired percentile (default is 90th percentile).
    
        Returns:
            The nth percentile value of the column, or None if the column is empty or non-numeric.
        """
        values = [row[column] for row in data if row[column] is not None and isinstance(row[column], (int, float))]
        if not values:
            return None
        return np.percentile(values, p)

    def type_mode(data: List[Dict[str, Any]], column: str) -> Any:
        """
        Calculate the mode (most frequent value) for a categorical column using NumPy.
    
        Args:
            data: List of dictionaries representing rows in the dataset.
            column: The column name for which to calculate the mode.
    
        Returns:
            The mode value of the column, or None if the column is empty.
        """
        values = [row[column] for row in data if row[column] is not None]
        if not values:
            return None
        return np.argmax(np.bincount(values))



