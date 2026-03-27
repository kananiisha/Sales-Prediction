#!/usr/bin/env python
"""
QUICK START GUIDE FOR BIGMART SALES PREDICTION APP
====================================================

Step 1: Install Dependencies
Run: pip install -r requirements.txt

Step 2: Initialize Database (if first time)
Run: python -c "from app import app, db; app.app_context().push(); db.create_all()"

Step 3: Start the Flask Server
Run: python app.py

Step 4: Access the App
Open browser and go to: http://localhost:5000

FIRST TIME USAGE:
1. Click "Sign Up"
2. Create an account (name, email, password)
3. Click "Login" and use your credentials
4. Click "Predict" to make a sales prediction
5. View results on the result page
6. Check "History" to see all your predictions
7. Visit "Dashboard" for analytics

TEST THE APP (Optional):
Run: python test_app.py
This will show all available routes and verify setup.

KEY ROUTES:
- http://localhost:5000/signup  → Create account
- http://localhost:5000/login   → Login page
- http://localhost:5000/dashboard → Main dashboard
- http://localhost:5000/predict → Make prediction
- http://localhost:5000/history → View all predictions
- http://localhost:5000/logout  → Logout

TROUBLESHOOTING:

Problem: ModuleNotFoundError: No module named 'flask'
Solution: Run pip install -r requirements.txt

Problem: Database error
Solution: Run: python -c "from app import app, db; app.app_context().push(); db.create_all()"

Problem: Port 5000 already in use
Solution: Change port in app.py line: app.run(debug=True, port=5001)

Problem: Model not found (rf_model.pkl)
Solution: Ensure rf_model.pkl exists in the project root directory

MORE INFO:
Read README.md for complete documentation

SECURITY NOTE:
Change SECRET_KEY in app.py before deploying to production!
Current setting: app.config['SECRET_KEY'] = 'your_secret_key_change_this'
"""

if __name__ == '__main__':
    print(__doc__)
    print("\n✅ Quick start guide loaded. Follow the steps above!")
