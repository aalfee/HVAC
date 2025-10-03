
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from .preprocessing import preprocess

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'hvac_model_v1.pkl')

def train():
    # Dummy training data: 100 samples, 3 features
    X = np.random.rand(100, 3)
    y = np.random.randint(0, 2, 100)  # Binary classification (normal/fault)
    # Fit and save scaler
    X_scaled = preprocess(X, fit=True)
    clf = RandomForestClassifier()
    clf.fit(X_scaled, y)
    joblib.dump(clf, MODEL_PATH)
    print(f'Model trained and saved to {MODEL_PATH}')

if __name__ == '__main__':
    train()
