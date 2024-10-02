import pdfplumber
import re
from prettytable import PrettyTable
import logging

logger = logging.getLogger(__name__)

def clean_parameter_name(name):
    words = name.split()
    cleaned_name = ' '.join(words[:4])
    cleaned_name = re.sub(r'[^\w\s]$', '', cleaned_name)
    return cleaned_name

def is_valid_test_result(test_name):
    invalid_texts = ['Om Clinical Lab', 'LAB ID', 'Sample Collection', 'Ref. By', 'Printed', 'Report Released', 'Sent By']
    return not any(text.lower() in test_name.lower() for text in invalid_texts)

def extract_blood_report_data(pdf_path):
    logger.info(f"Extracting data from PDF: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"

    logger.debug(f"Extracted text: {full_text[:500]}...")  # Log first 500 characters

    patient_info = {}
    test_results = []

    # Extract patient information
    patient_info_patterns = [
        r'Name\s*:\s*([\w\s.]+)',
        r'LAB ID\s*:\s*([\d]+)',
        r'Age\s*:\s*([\d]+)\s*Yrs',
        r'Sex\s*:\s*([MF])',
        r'Sample Collection\s*:\s*([\d/]+\s*[\d:]+)',
        r'Report Released\s*:\s*([\d/]+\s*[\d:]+)',
    ]

    for pattern in patient_info_patterns:
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            key = pattern.split(r'\s*:\s*')[0].replace(r'\s*', ' ').strip()
            patient_info[key] = match.group(1).strip()

    # Extract test results
    test_pattern = r'([\w\s.]+)\s*:\s*([\d.]+)\s*([\w/%^]+)\s*([\d.-]+\s*-\s*[\d.-]+\s*[\w/%^]+)'
    for match in re.finditer(test_pattern, full_text):
        test_name, value, unit, range_with_unit = match.groups()
        test_name = clean_parameter_name(test_name.strip())
        
        if not is_valid_test_result(test_name):
            continue
        
        test_results.append({
            'name': test_name,
            'value': value,
            'unit': unit,
            'range': range_with_unit
        })

    logger.info(f"Extracted patient info: {patient_info}")
    logger.info(f"Extracted {len(test_results)} test results")

    return patient_info, test_results

def display_results(patient_info, test_results):
    # Display patient information
    print("Patient Information:")
    print("=" * 50)
    for key, value in patient_info.items():
        print(f"{key}: {value}")
    print("=" * 50)
    print()

    # Display test results
    table = PrettyTable()
    table.field_names = ["Parameter", "Tested Value", "Unit", "Normal Range"]
    table.align = "l"  # Left-align all columns
    table.max_width["Parameter"] = 30
    table.max_width["Tested Value"] = 15
    table.max_width["Unit"] = 10
    table.max_width["Normal Range"] = 20

    for result in test_results:
        table.add_row([
            result['name'],
            result['value'],
            result['unit'],
            result['range']
        ])

    print(table)

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

    for result in test_results:
        table.add_row([
            result['name'],
            result['value'],
            result['unit'],
            result['range']
        ])

    output.append(str(table))
    return "\n".join(output)

def main():
    pdf_path = 'C:/Users/admin/Desktop/Health/Disease-Prediction/sample_pdfs/Raghuraj_Chaurasia.pdf'
    patient_info, test_results = extract_blood_report_data(pdf_path)
    display_results(patient_info, test_results)

if __name__ == "__main__":
    main()