def preprocess_data(df):
    # Fill missing values
    df.fillna({
        'severity': 0,
        'resource_needed': 0,
        'volunteers_needed': 0
    }, inplace=True)

    # Convert severity to integers
    df['severity'] = df['severity'].astype(int)

    return df