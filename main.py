import build.Debug.myocr as myocr
import argparse
import pytesseract
import time

parser = argparse.ArgumentParser(
                    prog='Image processor script',
                    description='Preprocesses an image for an OCR tool like EasyOCR',)
parser.add_argument('input', help='Your input image file')
parser.add_argument(
    'output',
    nargs='?',  # Makes the argument optional
    help='Your output text file where you want to extract text into'
)

args = parser.parse_args()
# Start the timer
start_time = time.time()
processed_image = myocr.process_image(args.input, "temp")
elapsed_time = time.time() - start_time
print(f'Time elapsed: {round(elapsed_time * 1000)} ms')
text = pytesseract.image_to_string(processed_image)
# Run OCR with specific PSM mode
print('OCR RESULT:')
# Example usage
if args.output:
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"OCR result written to {args.output}")
else:
    print("Output not provided. Text will not be written to a file.")