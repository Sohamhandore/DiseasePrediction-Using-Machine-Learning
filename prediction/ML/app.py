from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
import tempfile
from pdf_extractor import extract_blood_report_data, format_results
from disease_models import get_prediction

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    logger.info("Received upload request")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request headers: {dict(request.headers)}")
    logger.info(f"Request files: {request.files}")
    logger.info(f"Request form: {request.form}")

    if 'file' not in request.files:
        logger.error("No file part in the request")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    disease_type = request.form.get('disease_type', 'liver')  # Default to liver if not specified
    
    if file.filename == '':
        logger.error("No selected file")
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        try:
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                file.save(temp_file.name)
                temp_file_path = temp_file.name

            logger.info(f"Temporary file saved at: {temp_file_path}")

            # Extract data from the PDF
            patient_info, table_data = extract_blood_report_data(temp_file_path)
            logger.info("Data extracted from PDF")
            
            # Format the results
            formatted_results = format_results(patient_info, table_data)
            logger.info("Results formatted")

            # Convert test_results to a dictionary
            test_results_dict = {}
            for row in table_data:
                if len(row) >= 2:
                    try:
                        test_results_dict[row[0]] = float(row[1])
                    except ValueError:
                        logger.warning(f"Could not convert {row[1]} to float for {row[0]}")

            # Get predictions
            risk_level, message, results = get_prediction(disease_type, test_results_dict)
            logger.info("Predictions obtained")

            # Delete the temporary file
            os.unlink(temp_file_path)
            logger.info("Temporary file deleted")

            response = {
                'patient_info': patient_info,
                'table_data': table_data,
                'formatted_results': formatted_results,
                'risk_level': risk_level,
                'message': message,
                'abnormal_results': results['abnormal'],
                'normal_results': results['normal']
            }
            logger.info("Sending response")
            return jsonify(response)
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}", exc_info=True)
            return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500
    
    logger.error("Invalid file type")
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Server is running"}), 200

if __name__ == '__main__':
    app.run(debug=True)