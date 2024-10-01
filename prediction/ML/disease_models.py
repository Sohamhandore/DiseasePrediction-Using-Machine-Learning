import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)
    X = data.drop('target', axis=1)
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

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
kidney_data = load_and_preprocess_data('datasets/kidney_disease.csv')
liver_data = load_and_preprocess_data('datasets/LPD.csv')
heart_data = load_and_preprocess_data('datasets/CHD.csv')

kidney_model = train_model(kidney_data[0], kidney_data[2])
liver_model = train_model(liver_data[0], liver_data[2])
heart_model = train_model(heart_data[0], heart_data[2])

kidney_scaler = kidney_data[4]
liver_scaler = liver_data[4]
heart_scaler = heart_data[4]

def get_prediction(disease, test_results):
    if disease == 'kidney':
        prediction = predict_disease(kidney_model, kidney_scaler, test_results)
    elif disease == 'liver':
        prediction = predict_disease(liver_model, liver_scaler, test_results)
    elif disease == 'heart':
        prediction = predict_disease(heart_model, heart_scaler, test_results)
    else:
        raise ValueError("Invalid disease type")

    risk_level = get_risk_level(prediction[1])
    return risk_level

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
