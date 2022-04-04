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
Uses TRT_pose recognition and added functions to detect if the human is falling.  
This is still a work in progress and has some running bugs.

### Install
first follow the installation of trt_pose:  
https://github.com/NVIDIA-AI-IOT/trt_pose  

resnet18_baseline_att_224x224_A is needed in the root file of the project.  
This can be downloaded from: https://github.com/NVIDIA-AI-IOT/trt_pose  

### Usage
To check that modules are working run test/check.py
At the moment still a work in progress. First run init.py then human_pos.py.
When you have ran those then run shutdown.py.

### Maintainer(s)
Antti Lehtosalo @AnttiL120

### Credits
jaybdub John  
tokk-nv Chitoku Yato

### Thanks
Thank you jaybdub John and tokk-nv Chitoku YATO for making trt_pose.

### Contributing
Antti Lehtosalo @AnttiL120

### License

