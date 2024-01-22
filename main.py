import cv2
import os
import sys
import tempfile
from datetime import datetime
  
from google.cloud import storage
from google.cloud import bigquery

def save(file_name):
    print("saving name to db...")
    dt = str(datetime.now())
    client = bigquery.Client()
    table_id = "awentia-data-pipeline.DataVision.processed_files"
    job_config = bigquery.QueryJobConfig(destination=table_id)

    rows_to_insert = [
        {"filename": file_name, "datetime": dt}
    ]
    print(rows_to_insert)
    errors = client.insert_rows_json(table_id, rows_to_insert)              # Make an API request.
    if errors == []:
        print("new rows have been added.")
    else:
        print("encountered errors while inserting rows: {}".format(errors))

def exist(file_name):
    #print("checking if file exist already...")
    file_name = file_name.replace("/","_").replace(".","_")

    client = bigquery.Client()
    table_id = "awentia-data-pipeline.DataVision.processed_files"
    job_config = bigquery.QueryJobConfig(destination=table_id)

    QUERY = 'SELECT * FROM `DataVision.processed_files` WHERE `filename` = "'+file_name+'";' #buscar si filename ya estaba en la db
    print (QUERY)
    query_job = client.query((QUERY))                                       # API request
    rows = list(query_job.result())                                               # Waits for query to finish

    if (len(rows)>0):
            return True                                                     #si ya estaba, archivo existe, ya fue procesado antes
    return False



def extract_frames(input_file, output_folder,video_name=""):
    if(video_name==""):                                                     #if no video name provided, use name of temporary file
        video_name = os.path.splitext(os.path.basename(input_file))[0]
    print("extracting frames from "+video_name+"...")
    video_capture = cv2.VideoCapture(input_file)
    if not video_capture.isOpened():
        print("Error opening the video file.")
        return
    success, image = video_capture.read()
    count = 0
    
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
    print("getting videos...")
    client = storage.Client()
    blobs = []
    for blob in client.list_blobs(bucket, prefix=prefix):
        if(str(blob.name).endswith('.h265') and (not exist(blob.name))):
            #print (str(blob.name))
            blobs.append(blob)
    #TO-DO: filter out registries on table proccesed-files
    return blobs




if __name__ == "__main__":

    blobs = get_videos()

    file_name = blobs[0].name
    file_name = file_name.replace("/","_").replace(".","_")
    _, temp_local_filename = tempfile.mkstemp()
    
    # Download file from bucket.
    blobs[0].download_to_filename(temp_local_filename)
    output_folder = "output"
    extract_frames(temp_local_filename, output_folder,file_name)
    #print(exist(file_name))











