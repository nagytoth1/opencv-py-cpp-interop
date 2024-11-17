import cv2
import numpy as np
from easyocr import Reader
from ultralytics import YOLO
import re

# Load YOLO model trained for book covers
model = YOLO('best.pt')  # Replace 'best.pt' with the path to your trained model for book covers

# Initialize EasyOCR reader for text recognition in Hungarian
reader = Reader(['hu'])

# Load the book cover image
image_path = 'input/uj_cover.jpg'  # Replace with your book cover image path
image = cv2.imread(image_path)

# Use YOLO model to detect text areas on the book cover
results = model.predict(source=image, save=False, conf=0.25)

# Process each detected bounding box
for result in results:
    result_set = set()
    boxes = result.boxes.xyxy  # Get bounding boxes
    detected = False
    for box in boxes:
        if not detected:
            detected = True
        # Extract bounding box coordinates and convert to integers
        x1, y1, x2, y2 = map(int, box[:4])

        # Crop the detected text region
        text_region = image[y1:y2, x1:x2]

        # Convert to RGB for EasyOCR compatibility
        text_rgb = cv2.cvtColor(text_region, cv2.COLOR_BGR2RGB)

        # Use EasyOCR to read text from the region
        ocr_results = reader.readtext(text_rgb)
        # Extract and display recognized text for titles, authors, subtitles
        for detection in ocr_results:
            result_set.add(detection[1])
            # Draw bounding box and detected text on the original image
            # cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.putText(image, raw_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    print(result_set)
# Save or display the final image with annotations
# cv2.imshow("Book Cover Text Detection", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
