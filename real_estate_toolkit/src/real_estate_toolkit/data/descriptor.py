from dataclasses import dataclass
from typing import Dict, List, Union, Any, Tuple
import statistics

@dataclass
class Descriptor:
    data: List[Dict[str, Any]]

    def none_ratio(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
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
        columns_to_check = self._get_columns_to_check(columns, numeric_only=True)
        averages = {}

        for col in columns_to_check:
            values = [float(row[col]) for row in self.data if row.get(col) is not None]
            if values:
                averages[col] = sum(values) / len(values)
        return averages

    def median(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        columns_to_check = self._get_columns_to_check(columns, numeric_only=True)
        medians = {}

        for col in columns_to_check:
            values = [float(row[col]) for row in self.data if row.get(col) is not None]
            if values:
                medians[col] = statistics.median(values)
        return medians

    def percentile(self, columns: Union[List[str], str] = "all", percentile: int = 50) -> Dict[str, float]:
        columns_to_check = self._get_columns_to_check(columns, numeric_only=True)
        percentiles = {}

        for col in columns_to_check:
            values = [float(row[col]) for row in self.data if row.get(col) is not None]
            if values:
                values.sort()
                index = int(len(values) * (percentile / 100))
                percentiles[col] = values[min(index, len(values) - 1)]
        return percentiles
    
    def type_and_mode(self, columns: Union[List[str], str] = "all") -> Dict[str, Tuple[str, Any]]:
        columns_to_check = self._get_columns_to_check(columns)
        types_and_modes = {}

        for col in columns_to_check:
            non_none_values = [row[col] for row in self.data if row.get(col) is not None]
            if non_none_values:
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
        if not data:
            return {}

        columns = data[0].keys()
        column_data = {col: [] for col in columns}
    
        for row in data:
            for col in columns:
                column_data[col].append(row[col])

        none_ratios = {}
        for col, values in column_data.items():
            arr = np.array(values, dtype=object) 
            none_ratios[col] = np.sum(arr == None) / len(arr)  
    
        return none_ratios

    def average(data: List[Dict[str, Any]], column: str) -> float:
        values = [row[column] for row in data if row[column] is not None and isinstance(row[column], (int, float))]
        if not values:
            return None
        return np.mean(values)

    def median(data: List[Dict[str, Any]], column: str) -> float:
        values = [row[column] for row in data if row[column] is not None and isinstance(row[column], (int, float))]
        if not values:
            return None
        return np.median(values)

    def percentile(data: List[Dict[str, Any]], column: str, p: float = 90) -> float:
        values = [row[column] for row in data if row[column] is not None and isinstance(row[column], (int, float))]
        if not values:
            return None
        return np.percentile(values, p)

    def type_and_mode(data: List[Dict[str, Any]], column: str) -> Any:
        values = [row[column] for row in data if row[column] is not None]
        if not values:
            return None
        return np.argmax(np.bincount(values))



