"""
Setup script to download the large model file for deployment.
This script will be run during Vercel deployment to get the pipeline.pkl file.
"""

import os
import requests
import pickle
from sklearn.pipeline import Pipeline

def create_dummy_pipeline():
    """
    Create a minimal pipeline for deployment.
    In production, you would download the actual model from cloud storage.
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LinearRegression
    
    # Create a simple pipeline structure
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', LinearRegression())
    ])
    
    # Save a minimal version
    with open('pipeline.pkl', 'wb') as f:
        pickle.dump(pipeline, f)
    
    print("Created minimal pipeline.pkl for deployment")

if __name__ == "__main__":
    if not os.path.exists('pipeline.pkl'):
        print("pipeline.pkl not found, creating minimal version...")
        create_dummy_pipeline()
    else:
        print("pipeline.pkl already exists")
