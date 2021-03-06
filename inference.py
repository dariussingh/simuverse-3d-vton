import cv2
import matplotlib.pyplot as plt
import os
from os.path import exists, join, basename, splitext
import open3d as o3d 
import argparse

if __name__=='__main__':
    # initialize the parser
    parser = argparse.ArgumentParser()
    # add the parameters
    parser.add_argument('--input_data', help='Data Folder Name', default='input_data')
    args = parser.parse_args()
    input_data = args.input_data

    # create clothing mask
    img = cv2.imread(f'./m3d-vton/{input_data}/cloth/cloth@1=cloth_front.jpg')
    img= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img,200, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite(f'./m3d-vton/{input_data}/cloth-mask/cloth@1=cloth_front_mask.jpg', thresh)
    
    # creating image parse
    os.system(f"cp -r './m3d-vton/{input_data}/image/person@1=person_whole_front.png' './2D-Human-Parsing/demo_imgs'")
    os.chdir("2D-Human-Parsing")
    with open('./inference/img_list.txt', 'w') as f:
        f.write('../demo_imgs/person@1=person_whole_front.png')
    with open('./demo_imgs/img_list.txt', 'w') as f:
        f.write('../demo_imgs/person@1=person_whole_front.png')
    os.chdir("inference")
    os.system("bash demo.sh")
    os.chdir("..")
    os.chdir("..")
    os.system("cp -r './2D-Human-Parsing/parsing_result/train_parsing/demo_imgs/person@1=person_whole_front_label.png' './m3d-vton/{}/image-parse' ".format(input_data))
    
    # creating pose keypoints
    os.system(f"cp -r './m3d-vton/{input_data}/image/person@1=person_whole_front.png' './openpose/examples/media'")
    os.chdir("openpose")
    os.system(" ./build/examples/openpose/openpose.bin --video ./examples/media/person@1=person_whole_front.png --display 0 --render_pose 0 --face --hand --write_json output_json_folder/")
    os.chdir("..")
    os.system("cp -r './openpose/output_json_folder/person@1=person_whole_front_000000000000_keypoints.json' './m3d-vton/{}/pose/person@1=person_whole_front_keypoints.json'".format(input_data))
    
    # running inference
    os.chdir("m3d-vton")
    os.system(f"python3 util/data_preprocessing.py --MPV3D_root {input_data}")
    os.system(f"python3 test.py --model MTM --name MTM --dataroot {input_data} --datalist test_pairs --results_dir results")
    os.system(f"python3 test.py --model DRM --name DRM --dataroot {input_data} --datalist test_pairs --results_dir results")
    os.system(f"python3 test.py --model TFM --name TFM --dataroot {input_data} --datalist test_pairs --results_dir results")
    os.system(f"python3 rgbd2pcd.py --parse_root {input_data}/image-parse")
    
    # post processing pcd
    os.system("mkdir ./results/aligned/final_pcd")
    # load point cloud
    pcd = o3d.io.read_point_cloud('./results/aligned/pcd/test_pairs/person@1=person.ply')
    # normal estimation
    pcd.estimate_normals()
    pcd.orient_normals_consistent_tangent_plane(100)
    # poisson surface reconstruction
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
    # save mesh
    o3d.io.write_triangle_mesh('./results/aligned/final_pcd/person@1=person.ply', mesh)