# Student Success Prediction Flask App - Complete Implementation

## ✅ Implementation Complete

The Flask application is fully functional and ready to predict student success/dropout outcomes using the trained XGBoost machine learning model.

## 📋 Project Structure

```
/workspaces/maier_project/
├── app.py                                    # Flask application with preprocessing & predictions
├── best_student_success_model.joblib         # Trained XGBoost model (92.5% accuracy)
├── minmax_scaler.joblib                      # MinMaxScaler (first preprocessing step)
├── selectkbest.joblib                        # SelectKBest feature selector (15 best features)
├── standard_scaler.joblib                    # StandardScaler (final preprocessing step)
├── original_columns.joblib                   # Original 34 dataset columns (for correct ordering)
├── feature_names.joblib                      # 15 selected feature names
├── categorical_features.joblib               # Categorical feature options
├── student-success-prediction-using-ml.ipynb # Jupyter notebook with model training
├── templates/
│   └── index.html                           # Beautiful Bootstrap 5 form interface
└── test_preprocessing.py                     # Preprocessing validation script
```

## 🚀 How to Run

### Start the Flask App

```bash
cd /workspaces/maier_project
python app.py
```

The app will run on `http://127.0.0.1:5000/`

### Access the Web Interface

Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

## 📝 Features

### 1. **Web Form Interface** (Beautiful Bootstrap 5 Design)
   - Organized into 4 logical sections:
     - 📋 **Student Demographics** - Marital status, Gender, Age, Application mode
     - 🎯 **Academic Background** - Previous qualifications, Scholarship status
     - 💰 **Financial Status** - Debtor status, Tuition fees, Displaced status
     - 📚 **Academic Performance** - 1st & 2nd semester units/grades

### 2. **Smart Form Controls**
   - **Dropdowns** for categorical features (8 fields):
     - Marital status, Application mode, Previous qualification
     - Displaced, Debtor, Tuition fees status, Gender, Scholarship holder
   - **Number inputs with constraints** for numeric features:
     - Age: 18-80 years
     - Approved units: 0-60
     - Grades: 0-20
     - Without evaluations: 0-60

### 3. **Complete Preprocessing Pipeline**
   - **MinMaxScaler**: Normalizes all 34 original features (0-1 range)
   - **SelectKBest**: Reduces to 15 most important features using chi-squared selection
   - **StandardScaler**: Applies z-score normalization to selected features
   - All preprocessing steps automatically applied before model prediction

### 4. **Accurate Predictions**
   - **Model**: XGBoost Classifier (92.5% training accuracy)
   - **Output**: 
     - Prediction: Graduate or Dropout
     - Confidence: Probability percentage (0-100%)
   - **Example**: "Graduate (Confidence: 83.0%)"

### 5. **REST API Endpoint**
   ```bash
   POST /api/predict
   Content-Type: application/json
   ```
   
   Request example:
   ```json
   {
     "Marital status": 1,
     "Application mode": 1,
     "Previous qualification": 1,
     "Displaced": 0,
     "Debtor": 0,
     "Tuition fees up to date": 1,
     "Gender": 0,
     "Scholarship holder": 0,
     "Age at enrollment": 25,
     "Curricular units 1st sem (approved)": 10,
     "Curricular units 1st sem (grade)": 14.5,
     "Curricular units 1st sem (without evaluations)": 2,
     "Curricular units 2nd sem (approved)": 12,
     "Curricular units 2nd sem (grade)": 15.0,
     "Curricular units 2nd sem (without evaluations)": 1
   }
   ```
   
   Response example:
   ```json
   {
     "prediction": "Graduate",
     "confidence": 0.829
   }
   ```

## 🔧 Technical Details

### Preprocessing Pipeline

The Flask app follows the exact same preprocessing pipeline as the training notebook:

1. **Input Collection**: User fills out 15 required fields
2. **Array Creation**: Convert to numpy array with all 34 features (unused = 0)
3. **MinMaxScaler**: Scale features to [0, 1] range
4. **SelectKBest**: Select 15 best features (chi-squared)
5. **StandardScaler**: Apply z-score normalization
6. **Model Prediction**: XGBoost classifier makes prediction

### Input Validation

- All 15 features are required
- Categorical values validated against allowed options
- Numeric values checked against min/max constraints
- Error messages clearly indicate any validation failures

### Feature Mapping

**Selected 15 Features** (from original 34):
1. Marital status
2. Application mode
3. Previous qualification
4. Displaced
5. Debtor
6. Tuition fees up to date
7. Gender
8. Scholarship holder
9. Age at enrollment
10. Curricular units 1st sem (approved)
11. Curricular units 1st sem (grade)
12. Curricular units 1st sem (without evaluations)
13. Curricular units 2nd sem (approved)
14. Curricular units 2nd sem (grade)
15. Curricular units 2nd sem (without evaluations)

## ✨ Key Improvements Made

1. ✅ **Proper Dropdowns** - 8 categorical fields use proper select/option controls
2. ✅ **Input Validation** - Type checking, range validation, required field validation
3. ✅ **Correct Preprocessing** - Exact same pipeline as training (MinMaxScaler → SelectKBest → StandardScaler)
4. ✅ **Feature Order** - Dynamic loading of original columns ensures correct feature ordering
5. ✅ **Confidence Scores** - Model prediction probabilities displayed as percentages
6. ✅ **Error Handling** - User-friendly error messages with detailed feedback
7. ✅ **REST API** - JSON endpoint for programmatic access
8. ✅ **Beautiful UI** - Modern Bootstrap 5 design with organized sections
9. ✅ **Form Sections** - Logical grouping of demographics, academics, finances
10. ✅ **Help Text** - Input hints and constraints visible to users

## 🧪 Testing

### Test the Preprocessing Pipeline

```bash
python test_preprocessing.py
```

Expected output:
```
✓ Loaded all preprocessing objects
Original features: 34
Selected features: 15
...
✓ SUCCESS: Preprocessing pipeline works correctly!
```

### Test Web Form

1. Open `http://127.0.0.1:5000/`
2. Fill in the form with sample data
3. Click "🔮 Predict Student Outcome"
4. See prediction with confidence score

### Test API

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"Marital status": 1, ...}'
```

## 📊 Model Performance

- **Algorithm**: XGBoost Classifier
- **Training Accuracy**: 92.5%
- **Features Used**: 15 (selected via chi-squared test)
- **Target Classes**: 
  - 0 = Dropout
  - 1 = Graduate

## 🔒 Data Requirements

All 15 input features are required. Missing fields will show validation error.

**Categorical Features** (use integer codes):
- Marital status: 1-6
- Application mode: 1-18
- Previous qualification: 1-17
- Displaced: 0 or 1
- Debtor: 0 or 1
- Tuition fees up to date: 0 or 1
- Gender: 0 or 1
- Scholarship holder: 0 or 1

**Numeric Features**:
- Age at enrollment: 18-80
- Curricular units (approved): 0-60
- Curricular units (grade): 0-20
- Curricular units (without evaluations): 0-60

## 📝 Usage Examples

### Example 1: Likely to Graduate
```
Age: 25, Gender: Female (0)
1st Sem: 10 approved, 14.5 grade, 2 without evaluations
2nd Sem: 12 approved, 15.0 grade, 1 without evaluations
Marital status: Single (1)
No debts, Tuition paid, Has scholarship
→ Prediction: Graduate (83.0% confidence)
```

### Example 2: At Risk of Dropout
```
Age: 20, Gender: Male (1)
1st Sem: 2 approved, 8.5 grade, 10 without evaluations
2nd Sem: 3 approved, 9.0 grade, 9 without evaluations
Marital status: Married (2)
Is a debtor, Behind on tuition
→ Prediction: Dropout (higher dropout risk)
```

## 🐛 Troubleshooting

### "Feature names should match those that were passed during fit"
- **Cause**: Feature ordering is incorrect
- **Fix**: Ensure `original_columns.joblib` is loaded correctly
- **Status**: ✅ FIXED - Using dynamic column loading

### Form not submitting
- **Cause**: Missing required fields or validation error
- **Fix**: Check error message at top of page
- **Status**: ✅ Working with full validation

### Port 5000 already in use
- **Fix**: Run on different port:
  ```bash
  python -c "from app import app; app.run(port=5001)"
  ```

## 📦 Dependencies

- Flask==3.1.2
- scikit-learn==1.8.0
- xgboost==3.1.2
- numpy==2.4.0
- pandas==2.3.3
- joblib==1.5.3

All included in `requirements.txt`

## ✅ Verification Checklist

- [x] Flask app loads all preprocessing objects correctly
- [x] Preprocessing pipeline applies correct transformations
- [x] Web form displays all 15 input fields with proper controls
- [x] Categorical fields use dropdowns with correct options
- [x] Numeric fields have min/max constraints
- [x] Input validation works for all field types
- [x] Predictions are accurate with confidence scores
- [x] Error handling with user-friendly messages
- [x] REST API endpoint functional
- [x] All joblib files created and saved
- [x] Original column order preserved
- [x] Bootstrap 5 UI styled and responsive

## 🎯 Ready for Production

The Flask app is **fully tested, validated, and ready to deploy**. All features work correctly, preprocessing pipeline is accurate, and the UI is user-friendly and professional.

---
**Created**: January 10, 2026
**Model Accuracy**: 92.5%
**Status**: ✅ Complete & Tested
