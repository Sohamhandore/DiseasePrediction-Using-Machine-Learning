from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os
import traceback
import logging
from disease_models import get_prediction
from pdf_extractor import extract_blood_report_data, format_results

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def test():
    return jsonify({"message": "Server is running"}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    logger.info("Received upload request")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request headers: {request.headers}")
    logger.info(f"Request files: {request.files}")
    
    if 'file' not in request.files:
        logger.error("No file part in the request")
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        logger.error("No selected file")
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        try:
            logger.info(f"Processing file: {file.filename}")
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                file.save(temp_file.name)
                temp_file_path = temp_file.name

            logger.info(f"Temporary file saved at: {temp_file_path}")

            # Extract data from the PDF
            patient_info, test_results = extract_blood_report_data(temp_file_path)
            logger.info("Data extracted from PDF")
            
            # Format the results
            formatted_results = format_results(patient_info, test_results)
            logger.info("Results formatted")

            # Get predictions
            results = get_prediction(test_results)
            logger.info("Predictions obtained")

            # Delete the temporary file
            os.unlink(temp_file_path)
            logger.info("Temporary file deleted")

            response = {
                'formatted_results': formatted_results,
                'kidney_prediction': results['kidney'],
                'liver_prediction': results['liver'],
                'heart_prediction': results['heart'],
                'abnormal_results': results['abnormal'],
                'normal_results': results['normal']
            }
            logger.info("Sending response")
            return jsonify(response)
        except Exception as e:
            error_msg = f"Error processing PDF: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 500
    logger.error("Invalid file type")
    return jsonify({'error': 'Invalid file type'}), 400

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the exception
    logger.exception("An unhandled exception occurred:")
    # Return JSON instead of HTML for HTTP errors
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)