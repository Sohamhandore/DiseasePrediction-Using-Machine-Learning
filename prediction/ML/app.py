from flask import Flask, request, jsonify
from flask_cors import CORS
from text_ext import extract_blood_report_data
from disease_models import get_prediction
import tempfile
import os

app = Flask(__name__)
CORS(app)

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    disease_type = request.form.get('disease_type', 'liver')
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            patient_info, test_results = extract_blood_report_data(temp_file.name)
        os.unlink(temp_file.name)
        
        prediction = get_prediction(disease_type, test_results)
        
        return jsonify({
            'patient_info': patient_info,
            'test_results': test_results,
            'prediction': prediction
        })
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True)
