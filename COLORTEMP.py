import cv2
import numpy as np
import os
import glob

def detect_and_correct_temperature(input_folder, output_folder, target_temp):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = glob.glob(os.path.join(input_folder, '*.png'))
    if not image_files:
        print("No PNG images found in the directory.")
        return

    total_images = len(image_files)
    temp_data = []

    for index, image_path in enumerate(image_files):
        image = cv2.imread(image_path)
        if image is None:
            continue

        original_temp = calculate_color_temperature(image)
        corrected_image = adjust_color_balance(image, target_temp)

        cv2.imwrite(os.path.join(output_folder, os.path.basename(image_path)), corrected_image)

        new_temp = calculate_color_temperature(corrected_image)
        temp_data.append(
            f"{os.path.basename(image_path)}: Original Temp: {original_temp} K, Corrected Temp: {new_temp} K")

        progress = (index + 1) / total_images * 100
        print(f"Processing {index + 1}/{total_images} ({progress:.2f}%)")

    with open(os.path.join(output_folder, "temperature_data.txt"), 'w') as f:
        f.writelines("%s\n" % line for line in temp_data)

def calculate_color_temperature(image):
    avg_bgr = np.mean(image, axis=(0, 1))
    avg_temp = avg_bgr[2] / avg_bgr[0]
    return avg_temp * 1000

def kelvin_to_rgb(temp):
    temp = temp / 100
    if temp <= 66:
        r = 255
        g = temp
        g = 99.4708025861 * np.log(g) - 161.1195681661 if g > 0 else 0
        b = 0 if temp <= 19 else temp - 10
        b = 138.5177312231 * np.log(b) - 305.0447927307 if b > 0 else 0
    else:
        r = temp - 60
        r = 329.698727446 * (r ** -0.1332047592)
        g = temp - 60
        g = 288.1221695283 * (g ** -0.0755148492)
        b = 255

    return (int(np.clip(r, 0, 255)), int(np.clip(g, 0, 255)), int(np.clip(b, 0, 255)))

def adjust_color_balance(image, target_temp):
    r, g, b = kelvin_to_rgb(target_temp)
    kelvin_rgb = np.array([b / 255.0, g / 255.0, r / 255.0])

    corrected_image = cv2.transform(image, np.diag(kelvin_rgb))
    corrected_image = np.clip(corrected_image, 0, 255).astype('uint8')
    return corrected_image

target_temperature = 6488  # Example: Change to 6500 to test a specific temperature
input_folder = '02_Frames'
output_folder = 'COLOR_CORRECTED'

detect_and_correct_temperature(input_folder, output_folder, target_temperature)