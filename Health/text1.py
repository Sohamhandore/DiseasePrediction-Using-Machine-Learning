import pdfplumber
import re
import sys
import io

# Path to the blood test PDF
pdf_path = "sample_report.pdf"  
# Change the standard output encoding to utf-8 to handle special characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Function to extract text from each page of a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to find a specific test value in the text
def find_test_value(test_name, text):
    # Regular expression to match the test name followed by its value
    pattern = rf"{test_name}\s*[:\-]?\s*(\d+\.?\d*)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)  # Return the captured group (the value)
    else:
        return None  # Return None if the test is not found


# Extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Example: Find the value for "Glucose"
value = find_test_value("mcv", extracted_text)


# Print the result
if value:
    print(f"{value}")
else:
    print("not found.")
