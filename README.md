# Fall_detection_nano
Fall detection with Jetson nano and rasberry camera


## Table of Contents

- [Sections](#sections)
  - [Short Description](#short-description)
  - [Install](#install)
  - [Usage](#usage)
  - [Maintainers](#maintainers)
  - [Credits](#credits)
  - [Thanks](#thanks)
  - [Contributing](#contributing)
  - [License](#license)

## Sections

### Title
Fall Detection Nano


### Short Description
Fall detection with Jetson nano and rasberry camera.
Uses TRT_pose recognition and added functions to detect if the human has fallen.  
The function follows the nose, hips and ankles to see if they get too close to each other and changes the color if human is not standing anymore.
It does not take sitting in to account.  

This project is made with monitor, keyboard and mouse plugged in the jetson nano.

### Install
Pytorch, torchvision, torch2trt needs to be installed to jetson nano with jetpack installed before trt_pose can be installed. 
This project is made with Python 3.6.9.  

Jetpack:  
https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit 

Pytorch and torchvision:  
https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-10-now-available/72048 

torch2trt needs packaging before installation:
'''
pip3 install packaging  
'''

torch2trt and trt_pose:  
https://github.com/NVIDIA-AI-IOT/trt_pose  

resnet18_baseline_att_224x224_A model is needed in the root file of the project.  
This can be downloaded from: https://github.com/NVIDIA-AI-IOT/trt_pose  
The functionality can be checked with trt_pose/live_demo in jupytern notebook.  

Make sure gstreamer has been installed on the jetpack:  
'''
gst-inspect-1.0 --version  
'''

Then you can download this project from the source:  
https://github.com/AnttiL120/Fall_detection_nano  

### Usage
This project is made so the user has monitor, keyboard and mouse plugged in the jetson nano.  

To check that modules are installed correctly run test/check.py  
'''
python3 check.py
'''

First run init.py which saves an optimized version of the resnet18 baseline.  
'''
python3 init.py
'''

Then if you get no errors run the main.py with python3.
'''
python3 main.py
'''
This might take while because loading of the model takes a while.

### Maintainer(s)
Antti Lehtosalo @AnttiL120

### Credits

Credits to the makers of TRT_pose.  
jaybdub John  
tokk-nv Chitoku Yato  

### Thanks
Thank you jaybdub John and tokk-nv Chitoku YATO for making trt_pose and great starting demo.  
Thank you also to Nvidia and Dusty-nv for the great tutorials founded online.  
### Contributing
Antti Lehtosalo @AnttiL120

### License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
