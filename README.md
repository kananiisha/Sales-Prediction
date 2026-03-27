# BigMart Sales Prediction Web Application

A Flask-based web application that predicts retail sales using a trained Random Forest machine learning model with user authentication, prediction history, and analytics dashboard.

## 🎯 Features

### ✅ Authentication System
- **Sign Up**: Create new user accounts with email and password
- **Login/Logout**: Secure session-based authentication
- **Password Hashing**: Using werkzeug.security for secure password storage
- **Access Control**: Login required for all prediction features

### 📊 Prediction System
- **Sales Prediction**: Input item and outlet details to predict sales
- **ML Model**: Pre-trained Random Forest classifier (rf_model.pkl)
- **Form Validation**: Client and server-side validation
- **Result Display**: Detailed prediction results with input confirmation

### 📈 Dashboard
- **Statistics Cards**: Total predictions, average sales
- **Quick Access**: Last 5 predictions with quick links
- **Summary View**: Overview of user activity

### 📚 Prediction History
- **Full History Table**: All past predictions with details
- **Sortable Data**: View category, MRP, discount, location
- **Quick Details**: Links to view full details of any prediction

### 💾 Database
- **User Management**: Store user accounts with password hashing
- **Prediction History**: Track all user predictions with timestamps
- **SQLAlchemy ORM**: Clean, object-oriented database interface

## 📁 Project Structure

```
BMSP/
├── app.py                          # Main Flask application
├── rf_model.pkl                    # Trained Random Forest model
├── bigmart_sales_dataset.csv       # Training dataset
├── requirements.txt                # Python dependencies
├── templates/
│   ├── base.html                   # Base template with navbar
│   ├── signup.html                 # Sign up page
│   ├── login.html                  # Login page
│   ├── dashboard.html              # User dashboard
│   ├── predict.html                # Prediction form
│   ├── result.html                 # Prediction result
│   ├── history.html                # Prediction history
│   ├── 404.html                    # 404 error page
│   └── 500.html                    # 500 error page
└── bigmart_sales.db                # SQLite database (auto-created)
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 3. Run the Application
```bash
python app.py
```

The app will start at `http://localhost:5000`

### 4. Test the App
```bash
python test_app.py
```

## 📋 Usage

### Creating an Account
1. Go to Sign Up page
2. Enter Name, Email, and Password
3. Click "Sign Up" button
4. You'll be redirected to login page

### Making a Prediction
1. Login with your credentials
2. Click "Predict" in navigation bar
3. Fill in the form with:
   - **Item Details**: Category, MRP, Visibility, Fat Content
   - **Outlet Details**: Type, Size, Location, Establishment Year
   - **Promotion**: Festival Flag, Discount Percentage
4. Click "Make Prediction" button
5. View the predicted units sold

### Viewing History
- Click "History" in navbar to see all your predictions
- Click "View Details" on any prediction to see full information
- Access from dashboard: Shows last 5 predictions

### Dashboard Insights
- **Total Predictions**: Count of all predictions made
- **Average Predicted Sales**: Mean of all predicted units
- **Last 5 Predictions**: Quick table with recent predictions

## 🛢️ Database Schema

### User Table
```
id (Integer, Primary Key)
name (String)
email (String, Unique)
password_hash (String)
```

### Prediction Table
```
id (Integer, Primary Key)
user_id (Integer, Foreign Key → User.id)
item_category (String)
item_mrp (Float)
item_visibility (Float)
item_fat_content (String)
outlet_type (String)
outlet_size (String)
outlet_location_type (String)
outlet_establishment_year (Integer)
festival_flag (String)
discount_percentage (Float)
predicted_units_sold (Float)
timestamp (DateTime)
```

## 🔐 Security Features

- **Password Hashing**: Uses werkzeug.security.generate_password_hash
- **Session Management**: Flask sessions for user authentication
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **CSRF Protection Ready**: Template structure supports Flask-WTF
- **User Data Isolation**: Users can only view their own predictions

## 🎨 Frontend

- **Bootstrap 5**: Responsive design
- **Custom Styling**: Purple gradient theme
- **Form Validation**: HTML5 validation + server-side checks
- **Flash Messages**: Real-time user feedback
- **Mobile Responsive**: Works on desktop and mobile

## 📝 Routes Summary

| Route | Method | Auth Required | Purpose |
|-------|--------|---------------|---------|
| / | GET | No | Home (redirects to dashboard or login) |
| /signup | GET, POST | No | User registration |
| /login | GET, POST | No | User authentication |
| /logout | GET | Yes | Clear session and logout |
| /dashboard | GET | Yes | User dashboard with statistics |
| /predict | GET, POST | Yes | Prediction form and processing |
| /result/<id> | GET | Yes | Display prediction result |
| /history | GET | Yes | View all predictions |

## 🧪 Testing

Use the provided test script to verify setup:
```bash
python test_app.py
```

This will:
- ✅ Verify Flask app imports correctly
- ✅ Display all available routes
- ✅ Show database tables
- ✅ Confirm system is ready

## 💡 Key Code Highlights

### Authentication Decorator
```python
@login_required  # Use on any route requiring login
def predict():
    pass
```

### Model Loading (Lazy)
```python
def load_model():
    """Load model only when needed"""
    global _model
    if _model is not None:
        return _model
    # Load from file...
```

### Database Operations
```python
# Create prediction
prediction = Prediction(
    user_id=session['user_id'],
    **form_data,
    predicted_units_sold=result
)
db.session.add(prediction)
db.session.commit()
```

## 🛠️ Configuration

**In app.py**, update these for production:
```python
app.config['SECRET_KEY'] = 'change-this-to-random-string'  # IMPORTANT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bigmart_sales.db'
```

## 📦 Dependencies

- **flask**: Web framework
- **flask-sqlalchemy**: ORM and database
- **pandas**: Data manipulation
- **scikit-learn**: ML model support
- **joblib/pickle**: Model serialization
- **werkzeug**: Security utilities
- **numpy**: Numerical computing

## 🎓 Student-Friendly Notes

This code is designed to be:
- ✅ Easy to understand and modify
- ✅ Viva-ready with clear comments
- ✅ Not over-engineered
- ✅ Following Flask best practices
- ✅ Modular and maintainable

All major concepts are documented inline for easy comprehension.

## 🤝 Contributing

This is a learning project. Feel free to:
- Add more features
- Improve UI/UX
- Optimize database queries
- Add more prediction features

## 📞 Support

For issues with the application:
1. Check error messages in browser
2. Review Flask debug output in terminal
3. Verify all dependencies are installed
4. Ensure rf_model.pkl exists in project root
5. Check that database tables exist: `python test_app.py`

## 📄 License

Educational project for learning Flask and ML integration.

---

**Built with ❤️ using Flask + Machine Learning**

4. Open your browser and go to `http://127.0.0.1:5000/`

## Features

- Attractive web interface with Bootstrap styling
- Form inputs for all required features
- Real-time prediction via AJAX
- Backend API built with Flask

## Model Details

The model predicts "Units_Sold" based on features like Item_Category, Item_MRP, Item_Visibility, etc., using a Random Forest Regressor with preprocessing.