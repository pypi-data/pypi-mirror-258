# Check if table is a DataFrame or a string representing the file path
import numpy as np
import pandas as pd
import json
from typing import *


def to_ndarray(
        np_data: Union[str, np.ndarray]
) -> np.ndarray:
    """
    Ensures that the input is a NumPy array, either by loading it from a file or
    directly using the provided array.

    Args:
        np_data (Union[str, np.ndarray]): A NumPy array or a string representing the path to a NumPy array file.

    Returns:
        np.ndarray: The NumPy array.

    Raises:
        ValueError: If the input is not a NumPy array or a string representing a file path.
    """

    if isinstance(np_data, str):
        # Load the array if a path is provided
        np_data = np.load(np_data)
    elif isinstance(np_data, np.ndarray):
        np_data = np_data
    else:
        raise ValueError("Input must be a NumPy array or a string representing the file path.")

    return np_data


def to_dataframe(
        pd_data: Union[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Ensures that the input is a pandas DataFrame, either by loading it from a CSV file or
    directly using the provided DataFrame.

    Args:
        pd_data (Union[str, pd.DataFrame]): A pandas DataFrame or a string representing the path to a CSV file.

    Returns:
        pd.DataFrame: The pandas DataFrame.

    Raises:
        ValueError: If the input is not a pandas DataFrame or a string representing a file path.
    """

    if isinstance(pd_data, str):
        # Load the table if a path is provided
        pd_data = pd.read_csv(pd_data, header=0, low_memory=False)
    elif not isinstance(pd_data, pd.DataFrame):
        raise ValueError("Input must be a Pandas DataFrame or a string representing the file path.")

    return pd_data

def to_dict(
        dict_data: Union[str, Dict]
) -> pd.DataFrame:
    """
    Ensures that the input is a pandas DataFrame, either by loading it from a CSV file or
    directly using the provided DataFrame.

    Args:
        pd_data (Union[str, pd.DataFrame]): A pandas DataFrame or a string representing the path to a CSV file.

    Returns:
        pd.DataFrame: The pandas DataFrame.

    Raises:
        ValueError: If the input is not a pandas DataFrame or a string representing a file path.
    """

    if isinstance(dict_data, str):
        # Load the table if a path is provided
        with open(dict_data, 'r') as dict_file:
            dict_data = json.load(dict_file)

    elif not isinstance(dict_data, dict):
        raise ValueError("Input must be a Dictionary or a string representing the file path.")

    return dict_data
