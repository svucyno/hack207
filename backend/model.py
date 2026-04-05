import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import random

def load_or_train_model():
    model_path = "models/model.pkl"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        # return dummy feature size compatible with model
        dummy_X = pd.DataFrame(
            np.random.rand(10, model.n_features_in_), 
            columns=[f"Feature_{i}" for i in range(model.n_features_in_)]
        )
        return model, dummy_X
    
    # Fallback if no model is found
    # AssumeEMBER features for a fallback structure
    X, y = generate_synthetic_data()
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X, y)
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, model_path)
    return model, X

def generate_synthetic_data():
    n_samples = 5000
    n_features = 50
    X = pd.DataFrame(np.random.rand(n_samples, n_features), columns=[f"Feature_{i}" for i in range(n_features)])
    y = np.random.randint(0, 2, n_samples)
    return X, y

def get_dummy_features_for_inference(model, metadata):
    # Transform file metadata into basic numerical structure matching model input.
    # We will simulate feature distribution matching RandomForest expected behavior. 
    features = np.random.rand(1, model.n_features_in_)
    # Tie 'entropy' into the first few features to ensure SHAP picks it up meaningfully later.
    if metadata.get("entropy"):
        features[0][0] = metadata["entropy"] / 8.0 # Normalize 0-1
    return features
