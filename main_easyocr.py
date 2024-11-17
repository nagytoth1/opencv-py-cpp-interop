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
image_path = './output_cover/thick.jpg'  # Replace with your book cover image path
image = cv2.imread(image_path)

# Use YOLO model to detect text areas on the book cover
results = model.predict(source=image, save=False, conf=0.25)
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
# Process each detected bounding box
for result in results:
    detected_texts = []
    filtered_boxes = non_max_suppression_fast(np.asarray(result.boxes.xyxy), overlapThresh=0.5)
    filtered_boxes = sorted(filtered_boxes, key=lambda box: box[1])  # Sort by y1 coordinate to follow top to bottom
    detected = False
    for box in filtered_boxes:
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
            detected_texts.append(detection[1])
            # Draw bounding box and detected text on the original image
            # cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.putText(image, raw_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    print(detected_texts)


# Save or display the final image with annotations
# cv2.imshow("Book Cover Text Detection", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
