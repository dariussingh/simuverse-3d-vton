import cv2
import matplotlib.pyplot as plt
import os
from os.path import exists, join, basename, splitext
import open3d as o3d 

if __name__=='__main__':
    # m3d-vton
    os.system("git clone https://github.com/fyviezhao/m3d-vton")
    os.chdir(os.getcwd() + "/m3d-vton/pretrained")
    os.system("gdown https://drive.google.com/uc?id=1wpN-yfa1_MbezqkcLfVspa2jVTJV7bjN")
    os.system("unzip -o M3D-VTON.zip ")
    os.system("rm M3D-VTON.zip")
    os.system("mv latest_net_DRM.pth ./aligned/DRM/")
    os.system("mv latest_net_MTM.pth ./aligned/MTM/")
    os.system("mv latest_net_TFM.pth ./aligned/TFM/")
    os.system("cd ..")
    os.system("cd ..")

    # 2D human parsing
    os.system("git clone https://github.com/fyviezhao/2D-Human-Parsing")
    os.system("cd 2D-Human-Parsing/pretrained")
    os.system("gdown https://drive.google.com/uc?id=1cTYhbKbtrPfREVI_EkredmIq5WaT5GY6")
    os.system("cd ..")
    os.system("cd ..")

    # openpose
    git_repo_url = 'https://github.com/CMU-Perceptual-Computing-Lab/openpose.git'
    project_name = splitext(basename(git_repo_url))[0]
    if not exists(project_name):
      # see: https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/949
      # install new CMake becaue of CUDA10
      os.system("wget -q https://cmake.org/files/v3.13/cmake-3.13.0-Linux-x86_64.tar.gz")
      os.system("tar xfz cmake-3.13.0-Linux-x86_64.tar.gz --strip-components=1 -C /usr/local")
      # clone openpose
      os.system("git clone -q --depth 1 $git_repo_url")
      os.system("sed -i 's/execute_process(COMMAND git checkout master WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}\/3rdparty\/caffe)/execute_process(COMMAND git checkout f019d0dfe86f49d1140961f8c7dec22130c83154 WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}\/3rdparty\/caffe)/g' openpose/CMakeLists.txt")
      # install system dependencies
      os.system("apt-get -qq install -y libatlas-base-dev libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler libgflags-dev libgoogle-glog-dev liblmdb-dev opencl-headers ocl-icd-opencl-dev libviennacl-dev")
      # install python dependencies
      os.system("pip install -q youtube-dl")
      # build openpose
      os.system("cd openpose && rm -rf build || true && mkdir build && cd build && cmake .. && make -j`nproc`")