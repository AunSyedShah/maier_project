#!/usr/bin/env python3
"""
Test script to verify preprocessing works correctly.
"""

import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load preprocessing objects
MINMAX_SCALER = joblib.load(os.path.join(BASE_DIR, 'minmax_scaler.joblib'))
SELECTKBEST = joblib.load(os.path.join(BASE_DIR, 'selectkbest.joblib'))
STANDARD_SCALER = joblib.load(os.path.join(BASE_DIR, 'standard_scaler.joblib'))
FEATURE_NAMES = joblib.load(os.path.join(BASE_DIR, 'feature_names.joblib'))
ALL_ORIGINAL_FEATURES = joblib.load(os.path.join(BASE_DIR, 'original_columns.joblib'))

print("✓ Loaded all preprocessing objects")
print(f"Original features: {len(ALL_ORIGINAL_FEATURES)}")
print(f"Selected features: {len(FEATURE_NAMES)}")

# Create a test input with all required features
feature_dict = {
    'Marital status': 1,
    'Application mode': 1,
    'Previous qualification': 1,
    'Displaced': 0,
    'Debtor': 0,
    'Tuition fees up to date': 1,
    'Gender': 0,
    'Scholarship holder': 0,
    'Age at enrollment': 25,
    'Curricular units 1st sem (approved)': 10,
    'Curricular units 1st sem (grade)': 14.5,
    'Curricular units 1st sem (without evaluations)': 2,
    'Curricular units 2nd sem (approved)': 12,
    'Curricular units 2nd sem (grade)': 15.0,
    'Curricular units 2nd sem (without evaluations)': 1,
}

print("\nTest input features:")
for feat, val in feature_dict.items():
    print(f"  {feat}: {val}")

try:
    # Create input array in exact column order
    input_array = np.array([[feature_dict.get(feat, 0.0) for feat in ALL_ORIGINAL_FEATURES]])
    print(f"\n✓ Created input array with shape: {input_array.shape}")
    
    # Apply MinMaxScaler
    scaled = MINMAX_SCALER.transform(input_array)
    print(f"✓ MinMaxScaler output shape: {scaled.shape}")
    
    # Apply SelectKBest
    selected = SELECTKBEST.transform(scaled)
    print(f"✓ SelectKBest output shape: {selected.shape}")
    
    # Apply StandardScaler
    final = STANDARD_SCALER.transform(selected)
    print(f"✓ StandardScaler output shape: {final.shape}")
    
    print("\n✓ SUCCESS: Preprocessing pipeline works correctly!")
    print(f"Final preprocessed data: {final}")
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
