import cv2
import numpy as np
from ultralytics import YOLO
import pytesseract

def non_max_suppression_fast(boxes, overlapThresh):
    if len(boxes) == 0:
        return []
    
    boxes = np.array(boxes)
    pick = []

    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        overlap = (w * h) / area[idxs[:last]]

        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    return boxes[pick].astype("int")


# Specify the path to the Tesseract executable if it's not in your PATH
# Example for Windows:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load YOLO model
model = YOLO('best.pt')  # Replace 'best.pt' with the path to your trained model

image_path = './output_cover/thick.jpg'  # Replace with your image path
image = cv2.imread(image_path)

# Use YOLO model to detect license plates
results = model.predict(source=image, save=False, conf=0.25)

detected_texts = []
# Process each detected bounding box
for result in results:
    filtered_boxes = non_max_suppression_fast(np.asarray(result.boxes.xyxy), overlapThresh=0.5)
    filtered_boxes = sorted(filtered_boxes, key=lambda box: box[1]) # sort by y coordinates from top to bottom approach
    for box in filtered_boxes:
        # Extract bounding box coordinates and convert to integers
        x1, y1, x2, y2 = map(int, box[:4])

        # Crop the detected license plate region
        region = image[y1:y2, x1:x2]

        # Use PyTesseract to read text from the license plate region
        ocr_result = pytesseract.image_to_string(region, config='--psm 6')  # PSM 7 assumes a single line of text

        # Clean the recognized text
        cleaned_text = ocr_result.strip().split('\n') # remove unnecessary characters, line breaks
        if cleaned_text:
            for text in cleaned_text:
                detected_texts.append(text)
        # Draw bounding box and detected text on the original image if matched
        # cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # cv2.putText(image, cleaned_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    print(detected_texts)