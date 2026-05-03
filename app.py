from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pandas as pd
import os
import joblib
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bigmart_sales.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# ============== DATABASE MODELS ==============

class User(db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and store password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)

class Prediction(db.Model):
    """Prediction model to store user prediction history"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_category = db.Column(db.String(50), nullable=False)
    item_mrp = db.Column(db.Float, nullable=False)
    item_visibility = db.Column(db.Float, nullable=False)
    item_fat_content = db.Column(db.String(20), nullable=False)
    outlet_type = db.Column(db.String(30), nullable=False)
    outlet_size = db.Column(db.String(10), nullable=True)
    outlet_location_type = db.Column(db.String(20), nullable=False)
    outlet_establishment_year = db.Column(db.Integer, nullable=False)
    festival_flag = db.Column(db.String(10), nullable=False)
    discount_percentage = db.Column(db.Float, nullable=False)
    predicted_units_sold = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ============== MODEL LOADING ==============

MODEL_PATH = "rf_model.pkl"
_model = None

def load_model():
    """Load trained ML model (lazy loading)"""
    global _model
    if _model is not None:
        return _model
    if not os.path.exists(MODEL_PATH):
        print(f"Model file not found: {MODEL_PATH}")
        return None
    try:
        # Use joblib to load the model
        _model = joblib.load(MODEL_PATH)
        print(f"Model loaded successfully: {type(_model).__name__}")
        return _model
    except Exception as e:
        print(f"Error loading model with joblib: {e}")
        return None

# ============== AUTHENTICATION DECORATORS ==============

def login_required(f):
    """Decorator to require login for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ============== ROUTES ==============

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, else to login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User sign up route"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([name, email, password, confirm_password]):
            flash('All fields are required', 'danger')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('signup'))
        
        # Create new user
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Auto-login the user after signup
        session['user_id'] = user.id
        session['user_name'] = user.name
        flash(f'Account created successfully! Welcome, {user.name}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        # If user not found, redirect to signup
        if not user:
            flash(f'No account found with email: {email}. Please sign up first!', 'info')
            return redirect(url_for('signup'))
        
        # Check password
        if user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid password. Please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout route"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard showing user statistics"""
    user_id = session['user_id']
    predictions = Prediction.query.filter_by(user_id=user_id).all()
    
    total_predictions = len(predictions)
    last_5_predictions = sorted(predictions, key=lambda x: x.timestamp, reverse=True)[:5]
    
    avg_sales = 0
    if predictions:
        avg_sales = sum([p.predicted_units_sold for p in predictions]) / len(predictions)
    
    return render_template('dashboard.html', 
                         total_predictions=total_predictions,
                         last_5_predictions=last_5_predictions,
                         avg_sales=round(avg_sales, 2))

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    """Prediction form and processing"""
    if request.method == 'POST':
        try:
            # Get form data with lowercase names (for database storage)
            form_data = {
                'item_category': request.form.get('item_category'),
                'item_mrp': float(request.form.get('item_mrp')),
                'item_visibility': float(request.form.get('item_visibility')),
                'item_fat_content': request.form.get('item_fat_content'),
                'outlet_type': request.form.get('outlet_type'),
                'outlet_size': request.form.get('outlet_size'),
                'outlet_location_type': request.form.get('outlet_location_type'),
                'outlet_establishment_year': int(request.form.get('outlet_establishment_year')),
                'festival_flag': request.form.get('festival_flag'),
                'discount_percentage': float(request.form.get('discount_percentage'))
            }

            if form_data['item_category'] not in ['Food', 'Drinks']:
                form_data['item_fat_content'] = 'Non Edible'
            
            # Load model
            model = load_model()
            if model is None:
                flash('Model not available. Please contact admin.', 'danger')
                return redirect(url_for('predict'))
            
            # Map form data to model expected column names (PascalCase with underscores)
            # Festival_Flag needs to be integer (0 or 1) for the model
            model_input = {
                'Item_Category': form_data['item_category'],
                'Item_MRP': form_data['item_mrp'],
                'Item_Visibility': form_data['item_visibility'],
                'Item_Fat_Content': form_data['item_fat_content'],
                'Outlet_Type': form_data['outlet_type'],
                'Outlet_Size': form_data['outlet_size'],
                'Outlet_Location_Type': form_data['outlet_location_type'],
                'Outlet_Establishment_Year': form_data['outlet_establishment_year'],
                'Festival_Flag': int(form_data['festival_flag']),
                'Discount_Percentage': form_data['discount_percentage']
            }
            
            # Prepare data for prediction
            input_df = pd.DataFrame([model_input])
            
            # Make prediction
            prediction = model.predict(input_df)[0]
            
            # Store in database (using original form_data with lowercase keys)
            new_prediction = Prediction(
                user_id=session['user_id'],
                **form_data,
                predicted_units_sold=prediction
            )
            db.session.add(new_prediction)
            db.session.commit()
            
            flash(f'Prediction successful! Predicted units: {round(prediction, 2)}', 'success')
            return redirect(url_for('result', pred_id=new_prediction.id))
        
        except Exception as e:
            flash(f'Error during prediction: {str(e)}', 'danger')
            return redirect(url_for('predict'))
    
    return render_template('predict.html')

@app.route('/result/<int:pred_id>')
@login_required
def result(pred_id):
    """Display prediction result"""
    prediction = Prediction.query.get_or_404(pred_id)
    
    # Ensure user can only view their own predictions
    if prediction.user_id != session['user_id']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('result.html', prediction=prediction)

@app.route('/history')
@login_required
def history():
    """Display prediction history"""
    user_id = session['user_id']
    predictions = Prediction.query.filter_by(user_id=user_id).order_by(Prediction.timestamp.desc()).all()
    return render_template('history.html', predictions=predictions)

# ============== ERROR HANDLERS ==============

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# ============== CREATE TABLES ==============

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)