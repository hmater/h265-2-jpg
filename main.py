import cv2
import os
import sys


def extract_frames(input_file, output_path):
    video_capture = cv2.VideoCapture(input_file)
    if not video_capture.isOpened():
        print("Error opening the video file.")
        return
    success, image = video_capture.read()
    count = 0

    video_name = os.path.splitext(os.path.basename(input_file))[0]
    output_folder = output_folder + "/" + video_name
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    while success:
        frame_path = f"{output_path}/frame_{count:04d}.jpg"
        cv2.imwrite(frame_path, image)
        success, image = video_capture.read()
        count += 1

    video_capture.release()

def extract_frames(input_file, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(input_file)

    # Check if the file opened successfully
    if not cap.isOpened():
        print("Error opening the video file.")
        return

    # Get video information
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    print(f"FPS: {fps}")

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Extract and save each frame
    video_name = os.path.splitext(os.path.basename(input_file))[0]

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame as an image (PNG format, you can change the extension)
        output_file = f"{output_folder}/{video_name}_frame_{frame_count:04d}.png"
        cv2.imwrite(output_file, frame)

        frame_count += 1

    print(f"Total frames: {frame_count}")

    # Release the VideoCapture object
    cap.release()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py input_file_path")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_folder = "output"

    extract_frames(input_file_path, output_folder)
