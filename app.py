from flask import Flask, send_file, request
import os
from typing import List
import subprocess
import shutil

# app = FastAPI()

app = Flask(__name__)

@app.route('/')
def read_root():
    return {"Hello": "World"}

@app.route("/imageupload", methods=['POST'])
def root():

    try:
      # remove existing data
	os.system("rm -r './m3d-vton/results'")
      os.system("rm -r './m3d-vton/input_data'")
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

    cloth = request.files['cloth']
   # cloth file
    cloth.filename = "cloth@1=cloth_front.jpg"
    fileLocation = os.getcwd() + "/m3d-vton/input_data/cloth/" + cloth.filename
    with open(f'{fileLocation}', "wb") as buffer:
      shutil.copyfileobj(cloth, buffer)
    
    body = request.files['body']
    # body file
    body.filename = "person@1=person_whole_front.png"
    fileLocation = os.getcwd() + "/m3d-vton/input_data/image/" + body.filename
    with open(f'{fileLocation}', "wb") as buffer:
      shutil.copyfileobj(body, buffer)

    process = subprocess.Popen("python3 inference.py --input_data 'input_data'", shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.returncode)
    output_file_path = os.getcwd() + "/m3d-vton/results/aligned/TFM/test_pairs/tryon/person@1=person_whole_front.png"
    return send_file('./m3d-vton/results/aligned/TFM/test_pairs/tryon/person@1=person_whole_front.png')


if __name__ == '__main__':
    app.run(host="localhost", port=6001)
