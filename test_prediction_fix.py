#!/usr/bin/env python
"""Test prediction with fixed column names"""
from app import app, load_model
import pandas as pd

print("=" * 70)
print("TESTING PREDICTION WITH FIXED COLUMN NAMES")
print("=" * 70)

try:
    print("\n✅ Loading app...")
    print("✅ App loaded successfully")
    
    print("\n✅ Loading model...")
    model = load_model()
    print("✅ Model loaded")
    
    print("\n✅ Creating test data with correct column names...")
    test_data = {
        'Item_Category': 'Food', 
        'Item_MRP': 100.0, 
        'Item_Visibility': 0.5, 
        'Item_Fat_Content': 'Low Fat', 
        'Outlet_Type': 'Supermarket Type1', 
        'Outlet_Size': 'Small', 
        'Outlet_Location_Type': 'Tier 1', 
        'Outlet_Establishment_Year': 2010, 
        'Festival_Flag': 1, 
        'Discount_Percentage': 10.0
    }
    
    print("✅ Test data created with columns:")
    for col in test_data.keys():
        print(f"   - {col}: {test_data[col]}")
    
    print("\n✅ Creating DataFrame...")
    df = pd.DataFrame([test_data])
    print(f"✅ DataFrame shape: {df.shape}")
    print(f"✅ DataFrame columns: {list(df.columns)}")
    
    print("\n✅ Making prediction...")
    prediction = model.predict(df)[0]
    print(f"✅ PREDICTION SUCCESSFUL!")
    print(f"\n   Predicted Units Sold: {prediction:.2f}")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED - PREDICTION FIX WORKS!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
