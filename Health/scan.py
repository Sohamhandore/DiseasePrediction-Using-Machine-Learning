import os
from pdfminer.high_level import extract_text
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file. If the PDF contains scanned images, use OCR.
    """
    try:
        text = extract_text(pdf_path)
        if text.strip():  # If text extraction is successful
            return text
        else:
            raise ValueError("Empty text extracted, possibly a scanned document.")
    except Exception as e:
        print(f"Failed to extract text directly: {e}")
        # If direct text extraction fails, try OCR
        return ocr_pdf_images(pdf_path)

def ocr_pdf_images(pdf_path):
    """
    Perform OCR on the images in a PDF file to extract text.
    """
    from pdf2image import convert_from_path
    
    images = convert_from_path(pdf_path)
    text = ''
    
    for image in images:
        text += pytesseract.image_to_string(image)
        
    return text

def parse_health_parameters(extracted_text):
    """
    Parse health parameters like blood pressure, cholesterol, etc., from the extracted text.
    This function assumes a simple text-based report. For more complex formats,
    regular expressions or natural language processing techniques may be necessary.
    """
    parameters = {
        'blood_pressure': None,
        'cholesterol': None,
        'hemoglobin': None,
        'glucose': None,
    }

    # Example parsing logic - customize according to the actual format of the reports
    for line in extracted_text.split('\n'):
        if 'blood pressure' in line.lower():
            parameters['blood_pressure'] = extract_value(line)
        elif 'cholesterol' in line.lower():
            parameters['cholesterol'] = extract_value(line)
        elif 'hemoglobin' in line.lower():
            parameters['hemoglobin'] = extract_value(line)
        elif 'glucose' in line.lower():
            parameters['glucose'] = extract_value(line)
    
    return parameters

def extract_value(text_line):
    """
    Extract numeric value from a line of text.
    """
    import re
    match = re.search(r'\d+\.?\d*', text_line)
    if match:
        return float(match.group())
    return None

def process_pdf(pdf_path):
    """
    Full pipeline to process a PDF file and extract health parameters.
    """
    text = extract_text_from_pdf(pdf_path)
    health_parameters = parse_health_parameters(text)
    return health_parameters

# Example usage:
if __name__ == '__main__':
    pdf_path = 'path_to_your_uploaded_pdf_file.pdf'
    health_params = process_pdf(pdf_path)
    print(health_params)
