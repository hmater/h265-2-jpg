import cv2
import os
import sys
import tempfile
from datetime import datetime
  
from google.cloud import storage
from google.cloud import bigquery

def save(file_name):

    client = bigquery.Client()
    table_id = "awentia-data-pipeline.DataVision.processed_files"
    job_config = bigquery.QueryJobConfig(destination=table_id)
    sql = "INSERT INTO processed_files(filename, datetime) VALUES ("+file_name+","+datetime+")"
    query_job = client.query(sql, job_config=job_config)
    query_job.result()


def extract_frames(input_file, output_folder,video_name=""):
    video_capture = cv2.VideoCapture(input_file)
    if not video_capture.isOpened():
        print("Error opening the video file.")
        return
    success, image = video_capture.read()
    count = 0
    if(video_name==""):                                                     #if no video name provided, use name of temporary file
        video_name = os.path.splitext(os.path.basename(input_file))[0]
    output_folder = output_folder + "/" + video_name                        #adding folder named after the file
    os.makedirs(output_folder, exist_ok=True)                               #if folder doesnt exist, create it (always happening since folder addition)
    while success:
        frame_path = f"{output_folder}/frame_{count:04d}.jpg"
        cv2.imwrite(frame_path, image)
        success, image = video_capture.read()
        count += 1
    video_capture.release()
    save(video_name)


def get_videos(bucket = 'ap_test_collection_aw1_raw_input', prefix='1000000070d5eb51/2024/01/17/14'):
    client = storage.Client()
    blobs = []
    for blob in client.list_blobs(bucket, prefix=prefix):
        if(str(blob.name).endswith('.h265')):
            print (str(blob.name))
            blobs.append(blob)
    #TO-DO: filter out registries on table proccesed-files
    return blobs




if __name__ == "__main__":

    blobs = get_videos()

    file_name = blobs[0].name
    _, temp_local_filename = tempfile.mkstemp()
    
    # Download file from bucket.
    blobs[0].download_to_filename(temp_local_filename)
    output_folder = "output"
    extract_frames(temp_local_filename, output_folder,file_name)











