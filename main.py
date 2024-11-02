import build.Debug.myocr as myocr
import time
import argparse

parser = argparse.ArgumentParser(
                    prog='Image processor script',
                    description='Preprocesses an image for an OCR tool like EasyOCR',)
parser.add_argument('input', help='Your input image file')
args = parser.parse_args()
# Start the timer
start_time = time.time()

# Run the function
processed_image = myocr.process_image_v2(args.input, "temp2")

# Calculate the elapsed time
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time:.4f} seconds")