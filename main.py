import build.Release.myocr as myocr
import argparse
import time
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
parser.add_argument('--bounding', nargs='?', default='false', help='Display bounding box (true or false)')

args = parser.parse_args()

# Start the timer
fname = os.path.splitext(os.path.basename(args.input))[0]
out_dir_name = f"output_{fname}"
start_time = time.time()
if os.path.exists(out_dir_name):
    print('directory already exists!')
else:
    os.mkdir(out_dir_name)
myocr.process_image_v2(args.input, out_dir_name)
elapsed_time = time.time() - start_time
print(f'Time elapsed: {round(elapsed_time * 1000)} ms')