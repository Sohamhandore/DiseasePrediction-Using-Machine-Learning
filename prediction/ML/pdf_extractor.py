import re
import pdfplumber
import logging
from urllib.parse import unquote
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_blood_report_data(pdf_path):
    logger.info(f"Attempting to extract data from: {pdf_path}")
    
    if pdf_path.startswith('file:///'):
        pdf_path = unquote(pdf_path[8:])
    
    pdf_path = Path(pdf_path)
    
    patient_info = {}
    test_results = {}
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = "".join(page.extract_text() for page in pdf.pages)

        logger.info(f"Extracted {len(full_text)} characters of text")

        # Extract patient information
        patient_info_patterns = {
            'Name': r'Name\s*:\s*([\w\s]+)',
            'Lab No.': r'Lab No\.\s*:\s*([\d]+)',
            'Age': r'Age\s*:\s*([\d]+)\s*Years',
            'Gender': r'Gender\s*:\s*(Male|Female)',
            'Collected': r'Collected\s*:\s*([\d/]+\s*[\d:]+\s*[AP]M)',
            'Reported': r'Reported\s*:\s*([\d/]+\s*[\d:]+\s*[AP]M)',
        }

        for key, pattern in patient_info_patterns.items():
            match = re.search(pattern, full_text)
            if match:
                patient_info[key] = match.group(1).strip()

        logger.info(f"Extracted patient info: {patient_info}")

        # Extract test results
        test_pattern = r'(\w+(?:\s+\w+)*)\s+([\d.]+)\s+([\w/]+)'
        for match in re.finditer(test_pattern, full_text):
            test_name, value, unit = match.groups()
            if not any(word in test_name.lower() for word in ['note', 'ratio']):
                try:
                    test_results[test_name] = float(value)
                except ValueError:
                    logger.warning(f"Skipping invalid value for {test_name}: {value}")

        logger.info(f"Extracted {len(test_results)} test results")

    except Exception as e:
        logger.error(f"Error in extract_blood_report_data: {str(e)}", exc_info=True)
        raise

    return patient_info, test_results

def main():
    pdf_path = 'file:///C:/Users/admin/Downloads/sample_report.pdf'
    patient_info, test_results = extract_blood_report_data(pdf_path)
    
    print("Patient Information:")
    for key, value in patient_info.items():
        print(f"{key}: {value}")
    
    print("\nTest Results:")
    for test, value in test_results.items():
        print(f"{test}: {value}")

if __name__ == "__main__":
    main()
