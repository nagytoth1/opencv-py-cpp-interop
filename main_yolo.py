import cv2
import numpy as np
from ultralytics import YOLO
import pytesseract

# Specify the path to the Tesseract executable if it's not in your PATH
# Example for Windows:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load YOLO model
model = YOLO('best.pt')  # Replace 'best.pt' with the path to your trained model

image_path = './temp/thick.jpg'  # Replace with your image path
image = cv2.imread(image_path)

# Use YOLO model to detect license plates
results = model.predict(source=image, save=False, conf=0.25)

# Process each detected bounding box
for result in results:
    boxes = result.boxes.xyxy  # Get bounding boxes
    for box in boxes:
        # Extract bounding box coordinates and convert to integers
        x1, y1, x2, y2 = map(int, box[:4])

        # Crop the detected license plate region
        license_plate_region = image[y1:y2, x1:x2]

        # Convert to grayscale for Tesseract compatibility
        license_plate_gray = cv2.cvtColor(license_plate_region, cv2.COLOR_BGR2GRAY)

        # Use PyTesseract to read text from the license plate region
        ocr_result = pytesseract.image_to_string(license_plate_gray, config='--psm 6')  # PSM 7 assumes a single line of text

        # Clean the recognized text
        cleaned_text = ocr_result.strip()
        print("Cleaned License Plate Text:", cleaned_text)

        # Draw bounding box and detected text on the original image if matched
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, cleaned_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

# Save the final image with annotations
# output_path = 'annotated_license_plate.jpg'
# cv2.imwrite(output_path, image)
# print(f"Annotated image saved as {output_path}")

# Optionally display the final image with bounding boxes and text
resized = cv2.resize(image, (400,600))
cv2.imshow("License Plate Detection", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
