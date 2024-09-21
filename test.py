import sys
from pypdf import PdfReader

# creating a pdf reader object
reader = PdfReader('sample_report.pdf')

# initializing a variable to store all text
all_text = ""

# extracting text from each page and appending it to the variable
for i in range(len(reader.pages)):
    page = reader.pages[i]
    all_text += page.extract_text() + "\n"  # Adding a newline for separation between pages

# printing the combined text with UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')
print(all_text)