# ⚡ Quick Start Guide

## 🚀 Start the Flask App (30 seconds)

```bash
cd /workspaces/maier_project
python app.py
```

Your app will be running at: **http://127.0.0.1:5000/**

---

## 📝 Fill the Form (Example Values)

**Student Demographics:**
- Marital Status: Option 1 (Single)
- Gender: Female (0)
- Age at Enrollment: 25
- Application Mode: Mode 1

**Academic Background:**
- Previous Qualification: Qualification 1
- Scholarship Holder: Has Scholarship (1)

**Financial Status:**
- Debtor Status: Not a Debtor (0)
- Tuition Fees Up to Date: Yes (1)
- Displaced: Not Displaced (0)

**1st Semester:**
- Approved Units: 10
- Average Grade: 14.5
- Without Evaluations: 2

**2nd Semester:**
- Approved Units: 12
- Average Grade: 15.0
- Without Evaluations: 1

Click **"🔮 Predict Student Outcome"**

Expected Result: ✅ **Graduate (Confidence: 83.0%)**

---

## 🔌 Test the API

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

Expected Response:
```json
{
  "prediction": "Graduate",
  "confidence": 0.8295482993125916
}
```

---

## ✅ Verify Everything Works

```bash
# Test preprocessing pipeline
python test_preprocessing.py

# Run unit tests
pip install -r requirements.txt
pytest -q

# You can also initialize the database manually (optional):
python -c "from app import init_db; init_db()"

# Expected output: ✓ SUCCESS: Preprocessing pipeline works correctly!
```
---

## 📚 Features at a Glance

| Feature | Status | Notes |
|---------|--------|-------|
| Web Form | ✅ | Beautiful Bootstrap 5 UI |
| Dropdowns | ✅ | 8 categorical fields |
| Input Validation | ✅ | Type & range checking |
| Preprocessing | ✅ | Full 3-step pipeline |
| Predictions | ✅ | With confidence scores |
| REST API | ✅ | JSON endpoint available |
| Error Handling | ✅ | User-friendly messages |

---

## 🎯 What the App Does

1. **Takes Input**: Collects 15 student features via web form or API
2. **Validates**: Checks all fields for correct type/range
3. **Preprocesses**: Applies same pipeline as training:
   - MinMaxScaler (normalize 0-1)
   - SelectKBest (select 15 best features)
   - StandardScaler (z-score normalization)
4. **Predicts**: XGBoost model predicts Graduate/Dropout
5. **Returns**: Prediction with confidence percentage

---

## 📖 Learn More

- **Full Documentation**: See `FLASK_APP_DOCUMENTATION.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **Model Training**: See `student-success-prediction-using-ml.ipynb`

---

## 🆘 Troubleshooting

**Port 5000 already in use?**
```bash
python -c "from app import app; app.run(port=5001)"
```

**Get "Feature names" error?**
- Ensure `original_columns.joblib` exists
- Run: `python test_preprocessing.py`

**Form not submitting?**
- Check browser console for validation errors
- Ensure all 15 fields are filled

**API returns error?**
- Check all 15 fields are in JSON
- Verify field names exactly match form names

---

## ✨ That's It!

Your student success prediction app is ready to use. Just fill out the form or use the API to predict if a student will graduate or dropout with 92.5% accuracy! 🎓

---

**Created**: January 10, 2026  
**Model**: XGBoost (92.5% accuracy)  
**Status**: ✅ Production Ready
