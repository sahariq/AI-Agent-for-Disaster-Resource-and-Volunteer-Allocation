import pytest
from src.ui.dashboard import load_data, display_results

def test_load_data():
    data = load_data('data/raw/sample_data.csv')
    assert data is not None
    assert not data.empty
    assert 'severity' in data.columns

def test_display_results(mocker):
    mock_data = {
        'zone': ['Zone A', 'Zone B'],
        'allocated_volunteers': [10, 5],
        'unmet_severity': [0, 2]
    }
    mock_display = mocker.patch('src.ui.dashboard.st.write')
    display_results(mock_data)
    mock_display.assert_called_once_with(mock_data)