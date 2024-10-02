import pdfplumber
import re
from prettytable import PrettyTable
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def clean_parameter_name(name):
    words = name.split()
    cleaned_name = ' '.join(words[:4])
    cleaned_name = re.sub(r'[^\w\s]$', '', cleaned_name)
    return cleaned_name

def is_valid_test_result(test_name):
    invalid_texts = ['Om Clinical Lab', 'LAB ID', 'Sample Collection', 'Ref. By', 'Printed', 'Report Released', 'Sent By']
    return not any(text.lower() in test_name.lower() for text in invalid_texts)

def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def extract_blood_report_data(pdf_path):
    logger.info(f"Extracting data from PDF: {pdf_path}")
    patient_info = {}
    test_results = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"

        logger.debug(f"Extracted text: {full_text}")  # Log full extracted text

        # Extract patient information
        patient_info_patterns = [
            r'Name\s*:?\s*([\w\s.]+)',
            r'LAB ID\s*:?\s*([\d]+)',
            r'Age\s*:?\s*([\d]+)\s*(?:Yrs|Years)?',
            r'Sex\s*:?\s*([MF])',
            r'Sample Collection\s*:?\s*([\d/]+\s*[\d:]+)',
            r'Report Released\s*:?\s*([\d/]+\s*[\d:]+)',
        ]

        for pattern in patient_info_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                key = pattern.split(r'\s*:?\s*')[0].replace(r'\s*', ' ').strip()
                patient_info[key] = match.group(1).strip()

        logger.debug(f"Extracted patient info: {patient_info}")

        # Extract test results
        test_patterns = [
            r'([\w\s.]+)\s*:?\s*([\d.]+)\s*([\w/%^]+)\s*([\d.-]+\s*-\s*[\d.-]+\s*[\w/%^]+)',
            r'([\w\s.]+)\s*:?\s*([\d.]+)\s*([\w/%^]+)',  # For cases without normal range
        ]

        for pattern in test_patterns:
            for match in re.finditer(pattern, full_text):
                groups = match.groups()
                test_name = clean_parameter_name(groups[0].strip())
                
                if not is_valid_test_result(test_name):
                    continue
                
                if len(groups) == 4 and is_valid_number(groups[1]):
                    test_results.append([test_name, groups[1], groups[2], groups[3]])
                elif len(groups) == 3 and is_valid_number(groups[1]):
                    test_results.append([test_name, groups[1], groups[2], "N/A"])

        logger.debug(f"Extracted test results: {test_results}")

    except Exception as e:
        logger.error(f"Error extracting data from PDF: {str(e)}", exc_info=True)

    return patient_info, test_results

def format_results(patient_info, test_results):
    output = []
    
    # Format patient information
    output.append("Patient Information:")
    output.append("=" * 50)
    for key, value in patient_info.items():
        output.append(f"{key}: {value}")
    output.append("=" * 50)
    output.append("")

    # Format test results
    table = PrettyTable()
    table.field_names = ["Parameter", "Tested Value", "Unit", "Normal Range"]
    table.align = "l"  # Left-align all columns
    table.max_width["Parameter"] = 30
    table.max_width["Tested Value"] = 15
    table.max_width["Unit"] = 10
    table.max_width["Normal Range"] = 20

    for row in test_results:
        table.add_row(row)

    output.append(str(table))
    return "\n".join(output)

def main():
    pdf_path = 'C:/Users/admin/Desktop/Health/Disease-Prediction/sample_pdfs/sample_report.pdf'
    patient_info, test_results = extract_blood_report_data(pdf_path)
    formatted_output = format_results(patient_info, test_results)
    print(formatted_output)

if __name__ == "__main__":
    main()