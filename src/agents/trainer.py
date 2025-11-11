# File: /ai-agent-disaster-allocation/ai-agent-disaster-allocation/src/agents/trainer.py

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

class ModelTrainer:
    def __init__(self, data, target_column):
        self.data = data
        self.target_column = target_column
        self.model = RandomForestClassifier()

    def preprocess_data(self):
        X = self.data.drop(columns=[self.target_column])
        y = self.data[self.target_column]
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self):
        X_train, X_test, y_train, y_test = self.preprocess_data()
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        report = classification_report(y_test, predictions)
        return report

    def save_model(self, filename):
        import joblib
        joblib.dump(self.model, filename)

    def load_model(self, filename):
        import joblib
        self.model = joblib.load(filename)