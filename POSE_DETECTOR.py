import cv2
import os
from cvzone.PoseModule import PoseDetector

# Define folders
input_folder = 'COLOR_CORRECTED'
output_folder = 'POSED'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Initialize the pose detector
detector = PoseDetector()

# Get the list of images in the input folder
image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

total_images = len(image_files)  # Get the total number of images

for count, image_name in enumerate(image_files, start=1):
    img_path = os.path.join(input_folder, image_name)
    img = cv2.imread(img_path)

    if img is None:
        continue

    # Detect and draw the pose on the image
    img = detector.findPose(img)

    # Save the processed image to the output folder
    output_path = os.path.join(output_folder, image_name)
    cv2.imwrite(output_path, img)

    # Print progress in the console
    progress_percentage = (count / total_images) * 100  # Calculate the progress percentage
    print(f"Processing image {count}/{total_images} ({progress_percentage:.2f}%)")  # Display the progress

print("Finished processing all images.")
