import sys
sys.path.append("./build/Debug")  # Replace with the path to your build directory
import myocr

# Call the function
image_path = "./image.jpg"  # Replace with your actual image path
myocr.load_and_display_image(image_path)
