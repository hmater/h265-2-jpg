import cv2
import os
import sys
import tempfile
  
from google.cloud import storage


def extract_frames(input_file, output_folder):
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
        frame_path = f"{output_folder}/frame_{count:04d}.jpg"
        cv2.imwrite(frame_path, image)
        success, image = video_capture.read()
        count += 1

    video_capture.release()

if __name__ == "__main__":
    #if len(sys.argv) != 2:
        #print("Usage: python main.py input_file_path")
        #sys.exit(1)

    #input_file_path = sys.argv[1]
    output_folder = "output"

    client = storage.Client()
    for blob in client.list_blobs('ap_test_collection_aw1_raw_input', prefix='1000000070d5eb51/2024/01/17/14'):
        if(str(blob.name).endswith('.h265')):
            print (str(blob.name))
            video_gs = blob


    # temp = tempfile.NamedTemporaryFile()
    
    # try:
    #     temp.write(video_gs)
    #     output_folder = "output"
    #     extract_frames(temp, output_folder)
    # finally:
    #     temp.close()


    file_name = video_gs.name
    _, temp_local_filename = tempfile.mkstemp()
    temp = tempfile.NamedTemporaryFile()

    # Download file from bucket.
    
    video_gs.download_to_filename(temp_local_filename)
    output_folder = "output"
    extract_frames(temp_local_filename, output_folder)



    #input_file_path='gs://'+video_gs
    



    #extract_frames(input_file_path, output_folder)







