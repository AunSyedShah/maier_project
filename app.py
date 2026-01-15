from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import joblib
import numpy as np
import pandas as pd
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
# Application configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
csrf = CSRFProtect(app)

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the trained model
MODEL_PATH = os.path.join(BASE_DIR, 'best_student_success_model.joblib')
model = joblib.load(MODEL_PATH)

# Load preprocessing objects
MINMAX_SCALER = joblib.load(os.path.join(BASE_DIR, 'minmax_scaler.joblib'))
SELECTKBEST = joblib.load(os.path.join(BASE_DIR, 'selectkbest.joblib'))
STANDARD_SCALER = joblib.load(os.path.join(BASE_DIR, 'standard_scaler.joblib'))

# Load feature names and categorical mappings
FEATURE_NAMES = joblib.load(os.path.join(BASE_DIR, 'feature_names.joblib'))
CATEGORICAL_FEATURES = joblib.load(os.path.join(BASE_DIR, 'categorical_features.joblib'))

# Load original features in the correct order (must match training data)
ALL_ORIGINAL_FEATURES = joblib.load(os.path.join(BASE_DIR, 'original_columns.joblib'))

# --- User model for authentication ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def init_db():
    """Create (reset) database tables.

    Drops all tables and recreates them. This is useful for testing and dev
    environments to ensure a clean state.
    """
    db.drop_all()
    db.create_all()

# Define data type and range constraints for each feature
FEATURE_CONSTRAINTS = {
    'Marital status': {'type': 'categorical', 'values': CATEGORICAL_FEATURES['Marital status'], 'label': 'Marital Status'},
    'Application mode': {'type': 'categorical', 'values': CATEGORICAL_FEATURES['Application mode'], 'label': 'Application Mode'},
    'Previous qualification': {'type': 'categorical', 'values': CATEGORICAL_FEATURES['Previous qualification'], 'label': 'Previous Qualification'},
    'Displaced': {'type': 'categorical', 'values': CATEGORICAL_FEATURES['Displaced'], 'label': 'Displaced'},
    'Debtor': {'type': 'categorical', 'values': CATEGORICAL_FEATURES['Debtor'], 'label': 'Debtor Status'},
    'Tuition fees up to date': {'type': 'categorical', 'values': CATEGORICAL_FEATURES['Tuition fees up to date'], 'label': 'Tuition Fees Up to Date'},
    'Gender': {'type': 'categorical', 'values': CATEGORICAL_FEATURES['Gender'], 'label': 'Gender (0=Female, 1=Male)'},
    'Scholarship holder': {'type': 'categorical', 'values': CATEGORICAL_FEATURES['Scholarship holder'], 'label': 'Scholarship Holder'},
    'Age at enrollment': {'type': 'numeric', 'min': 18, 'max': 80, 'label': 'Age at Enrollment'},
    'Curricular units 1st sem (approved)': {'type': 'numeric', 'min': 0, 'max': 60, 'label': '1st Semester - Approved Units'},
    'Curricular units 1st sem (grade)': {'type': 'numeric', 'min': 0, 'max': 20, 'label': '1st Semester - Average Grade'},
    'Curricular units 1st sem (without evaluations)': {'type': 'numeric', 'min': 0, 'max': 60, 'label': '1st Semester - Units Without Evaluations'},
    'Curricular units 2nd sem (approved)': {'type': 'numeric', 'min': 0, 'max': 60, 'label': '2nd Semester - Approved Units'},
    'Curricular units 2nd sem (grade)': {'type': 'numeric', 'min': 0, 'max': 20, 'label': '2nd Semester - Average Grade'},
    'Curricular units 2nd sem (without evaluations)': {'type': 'numeric', 'min': 0, 'max': 60, 'label': '2nd Semester - Units Without Evaluations'},
}


def preprocess_input(feature_dict):
    """
    Preprocess input data using the same pipeline as training data.
    
    Args:
        feature_dict: Dictionary with feature names and values
    
    Returns:
        Preprocessed numpy array ready for model prediction
    """
    try:
        # Create input array in exact column order - CRITICAL FOR SCALERS
        # The scalers expect data in the same order as fit_transform received
        input_array = np.array([[feature_dict.get(feat, 0.0) for feat in ALL_ORIGINAL_FEATURES]])
        
        # Apply MinMaxScaler (trained on original 34 features)
        scaled = MINMAX_SCALER.transform(input_array)
        
        # Apply SelectKBest (extracts 15 best features)
        selected = SELECTKBEST.transform(scaled)
        
        # Apply StandardScaler (normalizes the 15 selected features)
        final = STANDARD_SCALER.transform(selected)
        
        return final
    except Exception as e:
        raise ValueError(f"Error during preprocessing: {str(e)}")


def validate_input(data):
    """
    Validate form input against constraints.
    
    Args:
        data: Dictionary with form data
    
    Returns:
        Tuple (is_valid, error_message)
    """
    for feature in FEATURE_NAMES:
        if feature not in data or data[feature] is None:
            return False, f"Missing value for {feature}"
        
        constraints = FEATURE_CONSTRAINTS.get(feature, {})
        value = data[feature]
        
        if constraints['type'] == 'categorical':
            if int(value) not in constraints['values']:
                return False, f"{feature}: Invalid value {value}. Allowed: {constraints['values']}"
        
        elif constraints['type'] == 'numeric':
            try:
                num_value = float(value)
                if num_value < constraints['min'] or num_value > constraints['max']:
                    return False, f"{feature}: Value {num_value} outside range [{constraints['min']}, {constraints['max']}]"
            except (ValueError, TypeError):
                return False, f"{feature}: Invalid numeric value"
    
    return True, None


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    prediction = None
    prediction_class = None
    error = None
    
    if request.method == 'POST':
        try:
            # Collect features from form
            input_dict = {}
            for fname in FEATURE_NAMES:
                value = request.form.get(fname)
                if value is not None:
                    if FEATURE_CONSTRAINTS[fname]['type'] == 'categorical':
                        input_dict[fname] = int(value)
                    else:
                        input_dict[fname] = float(value)
            
            # Validate input
            is_valid, error_msg = validate_input(input_dict)
            if not is_valid:
                error = error_msg
            else:
                # Preprocess input
                X_processed = preprocess_input(input_dict)
                
                # Make prediction
                pred = model.predict(X_processed)[0]
                pred_proba = model.predict_proba(X_processed)[0]
                
                prediction = 'Graduate' if pred == 1 else 'Dropout'
                prediction_class = 'success' if pred == 1 else 'danger'
                confidence = max(pred_proba) * 100
                
                prediction = f"{prediction} (Confidence: {confidence:.1f}%)"
        
        except Exception as e:
            error = f"Error making prediction: {str(e)}"
    
    return render_template(
        'index.html',
        feature_names=FEATURE_NAMES,
        feature_constraints=FEATURE_CONSTRAINTS,
        prediction=prediction,
        prediction_class=prediction_class,
        error=error
    )


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for making predictions via JSON."""
    try:
        data = request.get_json()
        
        # Validate input
        is_valid, error_msg = validate_input(data)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Preprocess input
        X_processed = preprocess_input(data)
        
        # Make prediction
        pred = model.predict(X_processed)[0]
        pred_proba = model.predict_proba(X_processed)[0]
        
        return jsonify({
            'prediction': 'Graduate' if pred == 1 else 'Dropout',
            'confidence': float(max(pred_proba))
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/profile')
@login_required
def profile():
    """Simple protected profile page for logged-in users."""
    return render_template('profile.html')

# Register blueprints
from auth import auth_bp
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    # Ensure database exists
    init_db()
    app.run(debug=True)
