import pandas as pd

def load_data(filepath: str, **kwargs) -> pd.DataFrame:
    """
    Loads a CSV file into a pandas DataFrame.
    
    Parameters:
    -----------
    filepath : str
        The path to the CSV file.
    **kwargs : dict
        Additional keyword arguments to pass to pandas.read_csv.
    
    Returns:
    --------
    pd.DataFrame
        The loaded DataFrame.
    """
    try:
        df = pd.read_csv(filepath, **kwargs)
        return df
    except Exception as e:
        raise IOError(f"Error loading file {filepath}: {e}")

def save_data(df: pd.DataFrame, filepath: str, **kwargs) -> None:
    """Save a DataFrame to a CSV file."""
    try:
        df.to_csv(filepath, index=False, **kwargs)
    except Exception as e:
        raise IOError(f"Error saving file {filepath}: {e}")



