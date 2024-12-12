import statistics
from typing import List, Dict, Any

def none_ratio(data: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Calculate the ratio of None (missing) values for each column in the dataset.
    
    Args:
        data: List of dictionaries representing rows in the dataset.
    
    Returns:
        A dictionary where keys are column names and values are the missing data ratio.
    """
    if not data:
        return {}
    
    column_counts = {key: 0 for key in data[0].keys()}
    none_counts = {key: 0 for key in data[0].keys()}
    
    for row in data:
        for key, value in row.items():
            column_counts[key] += 1
            if value is None:
                none_counts[key] += 1
    
    # Calculate the ratio of None values for each column
    ratio = {key: none_counts[key] / column_counts[key] for key in column_counts}
    return ratio

def average(data: List[Dict[str, Any]], column: str) -> float:
    """
    Calculate the average value for a numeric column in the dataset.
    
    Args:
        data: List of dictionaries representing rows in the dataset.
        column: The column name for which to calculate the average.
    
    Returns:
        The average value of the column, or None if the column is empty or non-numeric.
    """
    values = [float(row[column]) for row in data if row[column] is not None and isinstance(row[column], (int, float))]
    return statistics.mean(values) if values else None

def median(data: List[Dict[str, Any]], column: str) -> float:
    """
    Calculate the median value for a numeric column in the dataset.
    
    Args:
        data: List of dictionaries representing rows in the dataset.
        column: The column name for which to calculate the median.
    
    Returns:
        The median value of the column, or None if the column is empty or non-numeric.
    """
    values = [float(row[column]) for row in data if row[column] is not None and isinstance(row[column], (int, float))]
    return statistics.median(values) if values else None

def percentile(data: List[Dict[str, Any]], column: str, p: float = 90) -> float:
    """
    Calculate the nth percentile for a numeric column in the dataset.
    
    Args:
        data: List of dictionaries representing rows in the dataset.
        column: The column name for which to calculate the percentile.
        p: The desired percentile (default is 90th percentile).
    
    Returns:
        The nth percentile value of the column, or None if the column is empty or non-numeric.
    """
    values = [float(row[column]) for row in data if row[column] is not None and isinstance(row[column], (int, float))]
    return statistics.quantiles(values, n=100)[int(p)] if values else None

def type_mode(data: List[Dict[str, Any]], column: str) -> Any:
    """
    Calculate the mode (most frequent value) for a categorical column.
    
    Args:
        data: List of dictionaries representing rows in the dataset.
        column: The column name for which to calculate the mode.
    
    Returns:
        The mode value of the column, or None if the column is empty.
    """
    values = [row[column] for row in data if row[column] is not None]
    return statistics.mode(values) if values else None

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