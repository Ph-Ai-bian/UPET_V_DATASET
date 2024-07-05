from PIL import Image
import os

# Define folders
color_corrected_folder = 'COLOR_CORRECTED'
posed_folder = 'POSED'
output_folder = 'DRAWN'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# User-specified background color (example: light blue)
background_color = (0, 0, 200)  # Change this to the desired RGB color

# Get the list of images in the COLOR_CORRECTED folder
color_corrected_files = [f for f in os.listdir(color_corrected_folder) if os.path.isfile(os.path.join(color_corrected_folder, f))]

total_images = len(color_corrected_files)  # Get the total number of images

for count, image_name in enumerate(color_corrected_files, start=1):
    color_corrected_path = os.path.join(color_corrected_folder, image_name)
    posed_path = os.path.join(posed_folder, image_name)

    if not os.path.exists(posed_path):
        print(f"Skipping {image_name}: corresponding file not found in POSED folder.")
        continue

    color_corrected_image = Image.open(color_corrected_path).convert("RGBA")
    posed_image = Image.open(posed_path).convert("RGBA")

    # Create a new image for the differences with a transparent background
    differences_image = Image.new("RGBA", color_corrected_image.size, (0, 0, 0, 0))

    # Process each pixel
    for x in range(color_corrected_image.width):
        for y in range(color_corrected_image.height):
            pixel_color_corrected = color_corrected_image.getpixel((x, y))
            pixel_posed = posed_image.getpixel((x, y))

            # If the pixels are different, copy the pixel from the posed image to the differences image
            if pixel_color_corrected != pixel_posed:
                differences_image.putpixel((x, y), pixel_posed)

    # Create an image with the background color
    background_image = Image.new("RGBA", differences_image.size, background_color + (255,))

    # Composite the skeletons onto the background color
    combined_image = Image.alpha_composite(background_image, differences_image)

    # Save the combined image to the output folder
    output_path = os.path.join(output_folder, image_name)
    combined_image.save(output_path)

    # Print progress in the console
    progress_percentage = (count / total_images) * 100  # Calculate the progress percentage
    print(f"Processing image {count}/{total_images} ({progress_percentage:.2f}%)")  # Display the progress

print("Finished processing all images.")
