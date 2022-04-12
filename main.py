from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
from typing import List
import subprocess
import shutil

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/imageupload")
async def root(cloth: UploadFile, body:UploadFile):

    try:
      # remove existing data
      os.system("rm -r './m3d-vton/input_data'")
      os.system("rm -r './m3d-vton/results'")
      os.system("rm -r './2D-Human-Parsing/parsing_result'")
      os.system("rm -r './openpose/output_json_folder/person@1=person_whole_front_000000000000_keypoints.json'")
    except:
      pass

    # make new folder structure 
    os.mkdir('./m3d-vton/input_data')
    os.mkdir('./m3d-vton/input_data/cloth')
    os.mkdir('./m3d-vton/input_data/cloth-mask')
    os.mkdir('./m3d-vton/input_data/image')
    os.mkdir('./m3d-vton/input_data/image-parse')
    os.mkdir('./m3d-vton/input_data/pose')

    # rewriting text files
    with open('./m3d-vton/input_data/test_pairs.txt', 'w') as f:
      f.write('person@1=person_whole_front.png    cloth@1=cloth_front.jpg')
    with open('./m3d-vton/input_data/train_pairs.txt', 'w') as f:
      f.write('person@1=person_whole_front.png    cloth@1=cloth_front.jpg')

    # cloth file
    cloth.filename = "cloth@1=cloth_front.jpg"
    fileLocation = os.getcwd() + "/m3d-vton/input_data/cloth/" + cloth.filename
    with open(f'{fileLocation}', "wb") as buffer:
      shutil.copyfileobj(cloth.file, buffer)
    
    # body file
    body.filename = "person@1=person_whole_front.png"
    fileLocation = os.getcwd() + "/m3d-vton/input_data/image/" + body.filename
    with open(f'{fileLocation}', "wb") as buffer:
      shutil.copyfileobj(body.file, buffer)

    process = subprocess.Popen("python3 inference.py --input_data 'input_data'", shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.returncode)
    output_file_path = os.getcwd() + "/m3d-vton/results/aligned/TFM/test_pairs/tryon/person@1=person_whole_front.png"
    return FileResponse('./m3d-vton/results/aligned/TFM/test_pairs/tryon/person@1=person_whole_front.png')