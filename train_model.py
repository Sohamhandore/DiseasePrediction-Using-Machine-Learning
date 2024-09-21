import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Dummy dataset creation (replace this with your actual dataset)
data = {
    'blood_pressure': [120, 130, 140, 150, 110],
    'other_param': [1, 2, 1, 2, 1],
    'deficiency': [0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

# Features and target
X = df[['blood_pressure', 'other_param']]
y = df['deficiency']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))

# Save the model
joblib.dump(model, 'health_predictor_model.pkl')
