from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os
import traceback
import time
from disease_models import get_prediction
from pdf_extractor import extract_blood_report_data

app = Flask(__name__)
CORS(app)

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    start_time = time.time()
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    disease_type = request.form.get('disease_type', 'liver')
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        try:
            print(f"Starting PDF processing at {time.time() - start_time:.2f} seconds")
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                file.save(temp_file.name)
                print(f"Saved temporary file: {temp_file.name}")
                print(f"Starting data extraction at {time.time() - start_time:.2f} seconds")
                patient_info, test_results = extract_blood_report_data(temp_file.name)
            os.unlink(temp_file.name)
            
            print(f"Extracted patient info: {patient_info}")
            print(f"Extracted test results: {test_results}")
            print(f"Starting prediction at {time.time() - start_time:.2f} seconds")
            
            risk_level, message, results = get_prediction(disease_type, test_results)
            
            print(f"Finished processing at {time.time() - start_time:.2f} seconds")
            return jsonify({
                'patient_info': patient_info,
                'test_results': test_results,
                'risk_level': risk_level,
                'message': message,
                'abnormal_results': results['abnormal'],
                'normal_results': results['normal']
            })
        except Exception as e:
            error_msg = f"Error processing PDF: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            return jsonify({'error': error_msg}), 500
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True)
