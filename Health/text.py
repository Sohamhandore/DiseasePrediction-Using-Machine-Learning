import pdfplumber

# Path to the blood test PDF
pdf_path = "sample_report.pdf"
# Function to extract text from each page of a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text



# Extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Write the extracted text to a file with utf-8 encoding
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(extracted_text)

print("Text extracted and saved to extracted_text.txt")
