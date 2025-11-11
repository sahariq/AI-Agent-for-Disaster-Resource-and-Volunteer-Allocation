import pandas as pd

def load_data(file_path):
    """
    Load data from a CSV file or file-like object into a DataFrame.

    Parameters:
    - file_path: str or file-like object, path to the CSV file or uploaded file

    Returns:
    - DataFrame containing the loaded data
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
