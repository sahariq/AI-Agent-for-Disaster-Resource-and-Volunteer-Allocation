def read_csv(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def save_to_csv(dataframe, file_path):
    dataframe.to_csv(file_path, index=False)

def load_json(file_path):
    import json
    with open(file_path, 'r') as file:
        return json.load(file)

def save_to_json(data, file_path):
    import json
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)