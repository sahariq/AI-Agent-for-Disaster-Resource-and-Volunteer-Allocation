import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'multi-agent-system'))
from workers.worker_data_agent import DataWorkerAgent
import pandas as pd
import pytest

def test_load_data():
    agent = DataWorkerAgent('test_data_agent')
    df = agent.load_data('data/raw/sample_data.csv')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_preprocess_data():
    agent = DataWorkerAgent('test_data_agent')
    raw_data = {
        'id': [1, 2, 3],
        'severity': [None, 2, 3],
        'volunteers': [10, 20, None]
    }
    df = pd.DataFrame(raw_data)
    processed_df = agent.preprocess_data(df)

    assert processed_df['severity'].isnull().sum() == 0
    assert processed_df['volunteers'].isnull().sum() == 0
    assert processed_df['severity'].dtype == 'int64'
