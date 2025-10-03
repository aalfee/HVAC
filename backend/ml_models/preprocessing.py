
import numpy as np
from sklearn.preprocessing import StandardScaler

SCALER_PATH = __file__.replace('preprocessing.py', 'scaler.pkl')

def fit_scaler(X):
    scaler = StandardScaler()
    scaler.fit(X)
    import joblib
    joblib.dump(scaler, SCALER_PATH)
    return scaler

def load_scaler():
    import joblib
    import os
    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError('Scaler not found. Please fit first.')
    return joblib.load(SCALER_PATH)

def preprocess(X, fit=False):
    if fit:
        scaler = fit_scaler(X)
    else:
        scaler = load_scaler()
    return scaler.transform(X)
