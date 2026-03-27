from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
import pickle

app = Flask(__name__)

# Try to import joblib; if not available we'll fall back to pickle when loading the model
try:
    import joblib
    _use_joblib = True
except Exception:
    joblib = None
    _use_joblib = False

MODEL_PATH = "rf_model.pkl"
_model = None

def load_model():
    global _model
    if _model is not None:
        return _model
    if not os.path.exists(MODEL_PATH):
        return None
    # Prefer joblib if available
    if _use_joblib and joblib is not None:
        try:
            _model = joblib.load(MODEL_PATH)
            return _model
        except Exception:
            pass
    # Fallback to pickle
    try:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
            return _model
    except Exception:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    model = load_model()
    if model is None:
        return jsonify({'error': 'Model not available. Ensure rf_model.pkl exists and dependencies are installed.'}), 500
    data = request.get_json()
    # Expected input: dict with keys matching the features
    input_df = pd.DataFrame([data])
    try:
        prediction = model.predict(input_df)
    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'details': str(e)}), 500
    return jsonify({'predicted_units_sold': float(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)