import build.Debug.myocr as myocr
import argparse
import pytesseract
import time
import cv2
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


# processed_image = cv2.imread('./temp/bw_image.jpg')

# # Ensure processed_image is correctly read
# if processed_image is None:
#     print("Error: Processed image is not loaded correctly.")
#     exit(1)
# custom_config = r'--oem 3 --psm 11'  # You can experiment with psm 6, 11, etc.

# bounding_box = False

# def display_results_with_bounding_box():
#     # Run OCR with bounding box detection
#     data = pytesseract.image_to_data(processed_image, output_type=pytesseract.Output.DICT, config=custom_config)

#     # Check bounding boxes
#     n_boxes = len(data['text'])
#     result_text = ""

#     for i in range(n_boxes):
#         if int(data['conf'][i]) > 40:  # Adjust confidence level if needed
#             (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
#             cv2.rectangle(processed_image, (x, y), (x + w, y + h), (0, 0, 255), 5)
#             text = data['text'][i]
#             if text.strip():  # Avoid adding empty strings
#                 result_text += text + " "
#             print(f'Drawing box at ({x}, {y}, {w}, {h}) with confidence {data["conf"][i]}')

#     if args.output:
#         with open(args.output, 'w', encoding='utf-8') as f:
#             f.write(result_text.strip())  # Remove any trailing whitespace
#         print(f"OCR result written to {args.output}")
#     else:
#         print("Output not provided. Text will not be written to a file.")

#     # Optionally, print the final concatenated text
#     print("OCR Result:")
#     print(result_text)
#     # Resize for display
#     window_width, window_height = 500, 600
#     resized_image = cv2.resize(processed_image, (window_width, window_height))

#     # Display the image with bounding boxes
#     cv2.imshow("Detected Text with Bounding Boxes", resized_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# def display_results_with_bounding_box():
#     # Run OCR with bounding box detection
#     data = pytesseract.image_to_data(processed_image, output_type=pytesseract.Output.DICT, config=custom_config, lang="eng")

#     # Check bounding boxes
#     n_boxes = len(data['text'])
#     result_text = ""

#     for i in range(n_boxes):
#         if int(data['conf'][i]) > 40:  # Adjust confidence level if needed
#             (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
#             cv2.rectangle(processed_image, (x, y), (x + w, y + h), (0, 0, 255), 5)
#             text = data['text'][i]
#             if text.strip():  # Avoid adding empty strings
#                 result_text += text + " "
#             print(f'Drawing box at ({x}, {y}, {w}, {h}) with confidence {data["conf"][i]}')

#     if args.output:
#         with open(args.output, 'w', encoding='utf-8') as f:
#             f.write(result_text.strip())  # Remove any trailing whitespace
#         print(f"OCR result written to {args.output}")
#     else:
#         print("Output not provided. Text will not be written to a file.")

#     # Optionally, print the final concatenated text
#     print("OCR Result:")
#     print(result_text)
#     # Resize for display
#     window_width, window_height = 500, 600
#     resized_image = cv2.resize(processed_image, (window_width, window_height))

#     # Display the image with bounding boxes
#     cv2.imshow("Detected Text with Bounding Boxes", resized_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# def write_results_without_bounding_box():
#     result_text = pytesseract.image_to_string(processed_image, config=custom_config, lang="eng")
#     # Example usage
#     if args.output:
#         with open(args.output, 'w', encoding='utf-8') as f:
#             f.write(result_text)
#         print(f"OCR result written to {args.output}")
#     else:
#         print("Output not provided. Text will not be written to a file.")

# if __name__ == "__main__":
#     if args.bounding.lower() == 'true':
#         display_results_with_bounding_box()
#     else:
#         write_results_without_bounding_box()