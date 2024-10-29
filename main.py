import matplotlib.pyplot as plt
import build.Debug.myocr as myocr

# Use the C++ function to get a numpy image
processed_image = myocr.process_image("./image.jpg")
# Convert BGR to RGB by reversing the last dimension (color channels)
data_rgb = processed_image[..., ::-1]
plt.imshow(data_rgb)
plt.axis('off')
plt.show()