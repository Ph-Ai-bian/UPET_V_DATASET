import cv2  # Import the OpenCV library to handle video processing
import os   # Import the OS library to handle file path operations
import glob # Import glob to find files using patterns

# Function to extract frames from the video
def extract_frames(video_path, output_folder):
    # Check if the output folder exists, create it if it does not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extract the base name of the video file without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Open the video file
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # Get the total number of frames in the video

    success, image = video.read()  # Read the first frame
    count = 0  # Initialize frame count

    # Process frames until there are no more frames
    while success:
        frame_filename = os.path.join(output_folder, f"{video_name}_Frame_{count:02d}.png")  # Define filename for the frame
        cv2.imwrite(frame_filename, image)  # Save the current frame as a PNG file
        success, image = video.read()  # Read the next frame
        count += 1  # Increment the frame count

        # Print progress in the console
        progress_percentage = (count / total_frames) * 100  # Calculate the progress percentage
        print(f"Processing frame {count}/{total_frames} ({progress_percentage:.2f}%)")  # Display the progress

    # Release the video object
    video.release()
    print(f"Finished extracting frames from {video_name}.")

# Path to the video folder
video_folder = '01_Video'

# Find all video files in the video folder
video_files = glob.glob(os.path.join(video_folder, '*.*'))
if not video_files:
    raise FileNotFoundError("No video files found in the 'Video' folder.")

# Folder to save the extracted frames
output_folder = '02_Frames'

# Process each video file
for video_path in video_files:
    extract_frames(video_path, output_folder)
