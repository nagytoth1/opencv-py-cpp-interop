import cv2
import pytesseract
import argparse
import os

parser = argparse.ArgumentParser(
    prog='main.py',
    description='Preprocesses an image for an OCR tool like EasyOCR',
)
parser.add_argument('-i', '--input', 
    required=True,
    help='Your input image file')
parser.add_argument('-o', '--output', 
    nargs='?',  # Makes the argument optional
    help='Your output text file where you want to extract text into'
)
args = parser.parse_args()
image = cv2.imread(args.input)

result = pytesseract.image_to_string(image)
if not args.output:
    print(result)
else:
    with open(args.output, 'w+', encoding='utf-8') as file:
        file.write(result)
    print(f'Result saved to {args.output}!')