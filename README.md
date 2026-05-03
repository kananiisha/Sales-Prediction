# 🛒 BigMart Sales Prediction Web Application

A Flask-based web application that predicts retail sales using a trained **Random Forest** machine learning model — with user authentication, prediction history, and an analytics dashboard.

## 🎯 Features

- **Authentication** — Sign up, login, logout with secure password hashing
- **Sales Prediction** — Input item & outlet details to get predicted units sold
- **Dashboard** — View total predictions, average sales, recent activity
- **Prediction History** — Full table of all past predictions with details
- **Secure** — Session management, SQL injection prevention, user data isolation

## 📸 Screenshots

![Dashboard](screenshots/dashboard.png)
![Prediction Form](screenshots/predict.png)
![Results](screenshots/result.png)

---

## 🎯 Features

- **Authentication** — Sign up, login, logout with secure password hashing
- **Sales Prediction** — Input item & outlet details to get predicted units sold
- **Dashboard** — View total predictions, average sales, recent activity
- **Prediction History** — Full table of all past predictions with details
- **Secure** — Session management, SQL injection prevention, user data isolation

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Algorithm | Random Forest Regressor |
| R² Score | 0.8412 |
| RMSE | 15.95 |
| Features Used | 10 |

---

## 🏗️ Architecture

| Layer | Technology |
|-------|-----------|
| Frontend | Bootstrap 5 + Jinja2 Templates |
| Backend | Flask (Python) |
| Database | SQLite via SQLAlchemy ORM |
| ML Model | Random Forest (scikit-learn) |

---

## 📁 Project Structure

```
BigMart-Sales-Prediction/
├── app.py                      # Main Flask application
├── train_model.py              # Model training script
├── init_db.py                  # Database initializer
├── requirements.txt            # Python dependencies
├── random_forest_model.ipynb   # Model training notebook
├── screenshots/                # App screenshots
└── templates/
    ├── base.html               # Base layout with navbar
    ├── signup.html             # Registration page
    ├── login.html              # Login page
    ├── dashboard.html          # User dashboard
    ├── predict.html            # Prediction form
    ├── result.html             # Prediction result
    ├── history.html            # Prediction history
    ├── 404.html                # 404 error page
    └── 500.html                # 500 error page
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/kananiisha/Big-Mart-Sales-Prediction.git
cd Big-Mart-Sales-Prediction
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the Model
```bash
python train_model.py
```

### 4. Initialize Database
```bash
python init_db.py
```

### 5. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## 📝 API Routes

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/` | GET | No | Redirects to dashboard or login |
| `/signup` | GET, POST | No | User registration |
| `/login` | GET, POST | No | User authentication |
| `/logout` | GET | Yes | Clear session |
| `/dashboard` | GET | Yes | User dashboard |
| `/predict` | GET, POST | Yes | Prediction form |
| `/result/<id>` | GET | Yes | Prediction result |
| `/history` | GET | Yes | All predictions |

---

## 🛢️ Database Schema

**User**
```
id (PK) | name | email (unique) | password_hash | created_at
```

<<<<<<< HEAD
The model predicts "Units_Sold" based on features like Item_Category, Item_MRP, Item_Visibility, etc., using a Random Forest Regressor with preprocessing.
=======
**Prediction**
```
id (PK) | user_id (FK) | item_category | item_mrp | item_visibility
item_fat_content | outlet_type | outlet_size | outlet_location_type
outlet_establishment_year | festival_flag | discount_percentage
predicted_units_sold | timestamp
```

---

## 🔐 Security

- Password hashing via `werkzeug.security`
- Flask session-based authentication
- SQLAlchemy ORM prevents SQL injection
- Users can only access their own predictions
- Secret key loaded from environment variable

---

## 📦 Dependencies

```
flask
flask-sqlalchemy
pandas
scikit-learn
joblib
werkzeug
numpy
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License — free to use and modify.

---

**Built with ❤️ using Flask + Machine Learning**
>>>>>>> d36e9ff (Fix database schema migration and update app startup handling)
