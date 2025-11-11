from src.data.loader import load_data
from src.data.preprocess import preprocess_data
import pandas as pd
import pytest

def test_load_data():
    df = load_data('data/raw/sample_data.csv')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_preprocess_data():
    raw_data = {
        'id': [1, 2, 3],
        'severity': [None, 2, 3],
        'volunteers': [10, 20, None]
    }
    df = pd.DataFrame(raw_data)
    processed_df = preprocess_data(df)
    
    assert processed_df['severity'].isnull().sum() == 0
    assert processed_df['volunteers'].isnull().sum() == 0
    assert processed_df['severity'].dtype == 'int64'