from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import argparse
import os
import sys

# Create argument parser
parser = argparse.ArgumentParser(description="Convert images or PDFs to text using OCR.")
parser.add_argument("-input", required=True, help="Path to the input file (either image or PDF)")
parser.add_argument("-output", required=True, help="Path to the output text file")

# Parse arguments
args = parser.parse_args()
input_path = args.input
text_file_path = args.output

# Function to preprocess image
def preprocess_image(image):
    # Example preprocessing steps
    image = image.convert('L')  # Convert to grayscale
    return image

# Check if the input file exists
if not os.path.exists(input_path):
    print(f"Error: The file {input_path} does not exist.")
    sys.exit(1)

try:
    # Check if the input file is a PDF
    if input_path.lower().endswith('.pdf'):
        # Convert PDF to a list of images
        images = convert_from_path(input_path)
    else:
        # Open the image file
        images = [Image.open(input_path)]

    # Open the output text file
    with open(text_file_path, 'w') as file:
        # Iterate through the images and apply OCR
        for i, img in enumerate(images):
            img = preprocess_image(img)
            text = pytesseract.image_to_string(img)
            if len(images) > 1:  # For multi-page PDFs
                file.write(f'--- Page {i+1} ---\n')
            file.write(text)
            file.write('\n')  # Optional: Separate text from different pages with a newline

    print(f'Text has been successfully written to {text_file_path}')

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
