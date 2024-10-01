import re
import pdfplumber
from tabulate import tabulate

def extract_blood_report_data(pdf_path):
    if pdf_path.startswith('file:///'):
        pdf_path = pdf_path[8:]

    patient_info = {}
    test_results = []
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"

        # Extract patient information
        patient_info_patterns = [
            r'Name\s*:\s*([\w\s]+)',
            r'Lab No\.\s*:\s*([\d]+)',
            r'Age\s*:\s*([\d]+)\s*Years',
            r'Gender\s*:\s*(Male|Female)',
            r'Collected\s*:\s*([\d/]+\s*[\d:]+\s*[AP]M)',
            r'Reported\s*:\s*([\d/]+\s*[\d:]+\s*[AP]M)',
        ]

        for pattern in patient_info_patterns:
            match = re.search(pattern, full_text)
            if match:
                key = pattern.split(r'\s*:\s*')[0].replace(r'\s*', ' ').strip()
                patient_info[key] = match.group(1).strip()

        # Extract test results
        test_pattern = r'(\w+(?:\s+\w+)*)\s+([\d.]+)\s+([\w/]+)'
        for match in re.finditer(test_pattern, full_text):
            test_name, value, unit = match.groups()
            if not any(word in test_name.lower() for word in ['note', 'ratio']):
                test_results.append([test_name, value, unit])

    return patient_info, test_results

def main():
    pdf_path = 'file:///C:/Users/admin/Downloads/sample_report.pdf'
    patient_info, test_results = extract_blood_report_data(pdf_path)
    
    print("Patient Information:")
    for key, value in patient_info.items():
        print(f"{key}: {value}")
    
    print("\nTest Results:")
    print(tabulate(test_results, headers=['Test Name', 'Value', 'Unit'], tablefmt='grid'))

if __name__ == "__main__":
    main()
