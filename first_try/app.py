from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Make sure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/upload_reports', methods=['POST'])
def upload_reports():
    if 'patientReports' not in request.files:
        return jsonify({"error": "No files part"}), 400
    
    files = request.files.getlist('patientReports')
    reports = []

    for file in files:
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract health parameters from the PDF (example using process_pdf function)
        health_params = process_pdf(filepath)
        
        # Example prediction logic (you can replace with your actual model)
        criticality = calculate_criticality(health_params)
        
        reports.append({
            "filename": filename,
            "criticality": criticality
        })

    return jsonify(reports)

def process_pdf(filepath):
    # Dummy function to simulate processing
    # Replace this with your actual PDF processing logic
    return {
        'blood_pressure': 120,
        'cholesterol': 190,
        'hemoglobin': 13.5,
        'glucose': 85
    }

def calculate_criticality(health_params):
    # Dummy function to simulate criticality calculation
    # Replace this with your actual criticality calculation logic
    if health_params['blood_pressure'] > 140 or health_params['cholesterol'] > 240:
        return 'High'
    return 'Normal'

if __name__ == '__main__':
    app.run(debug=True)
