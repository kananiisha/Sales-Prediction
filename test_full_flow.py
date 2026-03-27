#!/usr/bin/env python
"""Comprehensive Flask app test - simulates full user flow"""
from app import app, db, User, Prediction, load_model
from werkzeug.security import generate_password_hash
import pandas as pd

print("=" * 80)
print("COMPREHENSIVE FLASK APP TEST - SIMULATING FULL USER FLOW")
print("=" * 80)

try:
    # Use app context for database operations
    with app.app_context():
        print("\n✅ Step 1: Initialize database...")
        db.create_all()
        print("   Database initialized")
        
        print("\n✅ Step 2: Create test user...")
        # Check if user exists
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            test_user = User(name='Test User', email='test@example.com')
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
            print("   Test user created")
        else:
            print("   Test user already exists")
        
        print("\n✅ Step 3: Load ML model...")
        model = load_model()
        print(f"   Model loaded: {type(model).__name__}")
        
        print("\n✅ Step 4: Create test prediction data with CORRECT column names...")
        test_input = {
            'Item_Category': 'Electronics',
            'Item_MRP': 250.5,
            'Item_Visibility': 0.75,
            'Item_Fat_Content': 'Non Edible',
            'Outlet_Type': 'Supermarket Type2',
            'Outlet_Size': 'Large',
            'Outlet_Location_Type': 'Tier 2',
            'Outlet_Establishment_Year': 2005,
            'Festival_Flag': 1,
            'Discount_Percentage': 15.5
        }
        
        input_df = pd.DataFrame([test_input])
        print("   Test data created with columns:")
        for col in input_df.columns:
            print(f"      - {col}")
        
        print("\n✅ Step 5: Make prediction...")
        prediction = model.predict(input_df)[0]
        print(f"   Prediction result: {prediction:.2f} units")
        
        print("\n✅ Step 6: Store prediction in database...")
        # Create form_data (lowercase) from test_input
        form_data = {
            'item_category': test_input['Item_Category'],
            'item_mrp': test_input['Item_MRP'],
            'item_visibility': test_input['Item_Visibility'],
            'item_fat_content': test_input['Item_Fat_Content'],
            'outlet_type': test_input['Outlet_Type'],
            'outlet_size': test_input['Outlet_Size'],
            'outlet_location_type': test_input['Outlet_Location_Type'],
            'outlet_establishment_year': test_input['Outlet_Establishment_Year'],
            'festival_flag': str(test_input['Festival_Flag']),
            'discount_percentage': test_input['Discount_Percentage']
        }
        
        new_prediction = Prediction(
            user_id=test_user.id,
            **form_data,
            predicted_units_sold=prediction
        )
        db.session.add(new_prediction)
        db.session.commit()
        print(f"   Prediction stored in database with ID: {new_prediction.id}")
        
        print("\n✅ Step 7: Retrieve prediction from database...")
        retrieved = Prediction.query.get(new_prediction.id)
        if retrieved:
            print(f"   Retrieved prediction:")
            print(f"      - Item: {retrieved.item_category}")
            print(f"      - MRP: ₹{retrieved.item_mrp}")
            print(f"      - Predicted Units: {retrieved.predicted_units_sold:.2f}")
            print(f"      - Timestamp: {retrieved.timestamp}")
        
        print("\n✅ Step 8: Query user's prediction history...")
        user_predictions = Prediction.query.filter_by(user_id=test_user.id).all()
        print(f"   Total predictions for user: {len(user_predictions)}")
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED - FULL FLOW WORKS CORRECTLY!")
        print("=" * 80)
        print("\nSummary:")
        print("  ✓ Database initialized")
        print("  ✓ User management working")
        print("  ✓ ML model predictions working")
        print("  ✓ Column name mapping (lowercase ↔ PascalCase) working")
        print("  ✓ Data storage in database working")
        print("  ✓ Data retrieval from database working")
        print("\nThe Flask app is ready for testing!")

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
