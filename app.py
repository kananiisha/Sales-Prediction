from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pandas as pd
import os
import joblib
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import inspect, text

# Load environment variables from .env file
load_dotenv()

# ============== APP INITIALIZATION ==============

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///bigmart_sales.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============== DATABASE MODELS ==============

class User(db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
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

# ============== DATABASE SCHEMA CHECK ==============

def ensure_database_schema():
    """Ensure the database schema matches the SQLAlchemy models."""
    with app.app_context():
        engine = db.get_engine()
        inspector = inspect(engine)

        # Create tables if they do not exist
        if not inspector.has_table('user') or not inspector.has_table('prediction'):
            db.create_all()
            return

        # Add missing created_at column to User table if needed
        user_columns = [col['name'] for col in inspector.get_columns('user')]
        if 'created_at' not in user_columns:
            with engine.connect() as conn:
                conn.execute(text('ALTER TABLE user ADD COLUMN created_at DATETIME'))
                conn.commit()


ensure_database_schema()

# ============== MODEL LOADING ==============

MODEL_PATH = "rf_model.pkl"
_model = None

def load_model():
    """Load trained ML model (lazy loading)"""
    global _model
    if _model is not None:
        return _model
    if not os.path.exists(MODEL_PATH):
        print(f"[ERROR] Model file not found: {MODEL_PATH}")
        return None
    try:
        _model = joblib.load(MODEL_PATH)
        print(f"[INFO] Model loaded: {type(_model).__name__}")
        return _model
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        return None

# ============== AUTHENTICATION ==============

def login_required(f):
    """Decorator to protect routes that require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ============== ROUTES ==============

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        if not all([name, email, password, confirm_password]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('signup'))

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))

        if User.query.filter_by(email=email).first():
            flash('An account with this email already exists.', 'danger')
            return redirect(url_for('signup'))

        # Create user
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        session['user_name'] = user.name
        flash(f'Welcome, {user.name}! Your account has been created.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not all([email, password]):
            flash('Email and password are required.', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('No account found with this email. Please sign up.', 'info')
            return redirect(url_for('signup'))

        if user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect password. Please try again.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    predictions = Prediction.query.filter_by(user_id=user_id).all()

    total_predictions = len(predictions)
    avg_sales = round(
        sum(p.predicted_units_sold for p in predictions) / total_predictions, 2
    ) if total_predictions > 0 else 0

    last_5_predictions = sorted(predictions, key=lambda x: x.timestamp, reverse=True)[:5]

    return render_template('dashboard.html',
                           total_predictions=total_predictions,
                           last_5_predictions=last_5_predictions,
                           avg_sales=avg_sales)


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        try:
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

            # Auto-fix fat content for non-food items
            if form_data['item_category'] not in ['Food', 'Drinks']:
                form_data['item_fat_content'] = 'Non Edible'

            # Load model
            model = load_model()
            if model is None:
                flash('Prediction model is unavailable. Please try again later.', 'danger')
                return redirect(url_for('predict'))

            # Map to model's expected column names
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

            input_df = pd.DataFrame([model_input])
            prediction_value = model.predict(input_df)[0]

            # Save prediction to DB
            new_prediction = Prediction(
                user_id=session['user_id'],
                **form_data,
                predicted_units_sold=round(float(prediction_value), 2)
            )
            db.session.add(new_prediction)
            db.session.commit()

            flash(f'Prediction complete! Estimated units sold: {round(prediction_value, 2)}', 'success')
            return redirect(url_for('result', pred_id=new_prediction.id))

        except ValueError as e:
            flash(f'Invalid input value: {str(e)}', 'danger')
            return redirect(url_for('predict'))
        except Exception as e:
            flash(f'Unexpected error: {str(e)}', 'danger')
            return redirect(url_for('predict'))

    return render_template('predict.html')


@app.route('/result/<int:pred_id>')
@login_required
def result(pred_id):
    prediction = Prediction.query.get_or_404(pred_id)

    # Security: users can only view their own predictions
    if prediction.user_id != session['user_id']:
        flash('You are not authorized to view this prediction.', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('result.html', prediction=prediction)


@app.route('/history')
@login_required
def history():
    user_id = session['user_id']
    predictions = Prediction.query.filter_by(user_id=user_id)\
                                  .order_by(Prediction.timestamp.desc()).all()
    return render_template('history.html', predictions=predictions)

# ============== ERROR HANDLERS ==============

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# ============== ENTRY POINT ==============

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False') == 'True')