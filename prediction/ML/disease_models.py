import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Current working directory:", os.getcwd())

def load_and_preprocess_data(file_name):
    full_path = os.path.join(os.getcwd(), file_name)
    print(f"Attempting to open file: {full_path}")
    
    data = pd.read_csv(file_name)
    print(data.columns)  # Add this line to see what columns are actually in your data
    
    # Check if 'target' column exists, if not, use the last column as target
    if 'target' in data.columns:
        X = data.drop('target', axis=1)
        y = data['target']
    else:
        X = data.iloc[:, :-1]  # All columns except the last one
        y = data.iloc[:, -1]   # The last column
    
    # Identify numeric and categorical columns
    numeric_columns = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_columns = X.select_dtypes(include=['object']).columns

    # Encode categorical variables
    le = LabelEncoder()
    for col in categorical_columns:
        X[col] = le.fit_transform(X[col].astype(str))

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale only the numeric columns
    scaler = StandardScaler()
    X_train[numeric_columns] = scaler.fit_transform(X_train[numeric_columns])
    X_test[numeric_columns] = scaler.transform(X_test[numeric_columns])

    return X_train, X_test, y_train, y_test, scaler

def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def predict_disease(model, scaler, test_results):
    test_data = pd.DataFrame([test_results])
    test_data_scaled = scaler.transform(test_data)
    prediction = model.predict_proba(test_data_scaled)[0]
    return prediction

# Load and train models
kidney_data = load_and_preprocess_data('C:/Users/admin/Desktop/Health/Disease-Prediction/datasets/kidney_disease.csv')
liver_data = load_and_preprocess_data('C:/Users/admin/Desktop/Health/Disease-Prediction/datasets/Liver Patient Dataset (LPD)_train.csv')
heart_data = load_and_preprocess_data('C:/Users/admin/Desktop/Health/Disease-Prediction/datasets/CHD_preprocessed.csv')

kidney_model = train_model(kidney_data[0], kidney_data[2])
liver_model = train_model(liver_data[0], liver_data[2])
heart_model = train_model(heart_data[0], heart_data[2])

kidney_scaler = kidney_data[4]
liver_scaler = liver_data[4]
heart_scaler = heart_data[4]

DISEASE_SPECIFIC_TESTS = {
    'liver': ['ALT', 'AST', 'ALP', 'GGT', 'Bilirubin', 'Albumin', 'Total Protein'],
    'heart': ['Cholesterol', 'Triglycerides', 'HDL', 'LDL', 'CRP', 'Troponin'],
    'kidney': ['Creatinine', 'BUN', 'eGFR', 'Sodium', 'Potassium', 'Calcium', 'Phosphorus']
}

THRESHOLDS = {
    'liver': {'ALT': 50, 'AST': 40, 'ALP': 120, 'GGT': 60, 'Bilirubin': 1.2, 'Albumin': 3.5, 'Total Protein': 6.0},
    'heart': {'Cholesterol': 200, 'Triglycerides': 150, 'HDL': 40, 'LDL': 100, 'CRP': 3, 'Troponin': 0.04},
    'kidney': {'Creatinine': 1.2, 'BUN': 20, 'eGFR': 60, 'Sodium': 135, 'Potassium': 3.5, 'Calcium': 8.5, 'Phosphorus': 2.5}
}

def get_prediction(disease, test_results):
    logger.info(f"Predicting for disease: {disease}")
    logger.info(f"Test results received: {test_results}")
    abnormal_results = []
    normal_results = []
    risk_level = "Normal"

    relevant_tests = DISEASE_SPECIFIC_TESTS.get(disease, [])
    
    for test, value in test_results.items():
        if test in relevant_tests and test in THRESHOLDS[disease]:
            threshold = THRESHOLDS[disease][test]
            result = {
                'test': test,
                'value': value,
                'threshold': threshold
            }
            if value > threshold:
                abnormal_results.append(result)
                risk_level = "At Risk"
            else:
                normal_results.append(result)

    if len(abnormal_results) > 2:
        risk_level = "High Risk"

    if not abnormal_results:
        message = f"Based on the available data, no significant risk factors for {disease} disease were identified. All tested parameters are within normal range."
    else:
        abnormal_details = [f"{result['test']} ({result['value']}, normal range: up to {result['threshold']})" for result in abnormal_results]
        message = f"The following values are above normal range for {disease} disease: {', '.join(abnormal_details)}. "
        if risk_level == "At Risk":
            message += f"This suggests a potential risk of {disease} disease. Please consult a doctor for a thorough evaluation."
        else:
            message += f"This indicates a high risk of {disease} disease. It is strongly recommended to consult a doctor immediately."

    logger.info(f"Prediction complete. Risk level: {risk_level}")
    return risk_level, message, {'abnormal': abnormal_results, 'normal': normal_results}

def get_risk_level(probability):
    if probability < 0.2:
        return "Normal"
    elif probability < 0.4:
        return "Low Risk"
    elif probability < 0.6:
        return "Moderate Risk"
    elif probability < 0.8:
        return "High Risk"
    else:
        return "Critical"