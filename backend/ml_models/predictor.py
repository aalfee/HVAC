
import numpy as np
import joblib
import os
from .preprocessing import preprocess

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'hvac_model_v1.pkl')

def predict(sensor_data):
    # sensor_data: list or np.array of shape (n_samples, 3)
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError('Trained model not found. Please train first.')
    try:
        X = np.array(sensor_data)
        X_scaled = preprocess(X, fit=False)
        clf = joblib.load(MODEL_PATH)
        preds = clf.predict(X_scaled)
        return preds.tolist()
    except Exception as e:
        raise RuntimeError(f'Prediction failed: {e}')

if __name__ == '__main__':
    # Example usage
    test_data = np.random.rand(2, 3)
    print('Predictions:', predict(test_data))
