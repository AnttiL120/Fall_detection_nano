#First run init.py with a command python3 init.py
#Init saves an optimized model "resnet18_baseline_att_224x224_A_epoch_249_trt.pth" to the project

import json
import trt_pose.coco
import torch
from torch2trt import TRTModule
import cv2
import torchvision.transforms as transforms
import PIL.Image
from draw import DrawObjects
from trt_pose.parse_objects import ParseObjects
from jetcam.csi_camera import CSICamera
from jetcam.utils import bgr8_to_jpeg
import numpy as np


#Topology for human pose
with open('human_pose.json', 'r') as f:
    human_pose = json.load(f)
topology = trt_pose.coco.coco_category_to_topology(human_pose)

#Resolution on the model was 224x224 so using the same
WIDTH = 224
HEIGHT = 224
data = torch.zeros((1, 3, HEIGHT, WIDTH)).cuda()

#Loading optimizied model
OPTIMIZED_MODEL = 'resnet18_baseline_att_224x224_A_epoch_249_trt.pth'
model_trt = TRTModule()
model_trt.load_state_dict(torch.load(OPTIMIZED_MODEL))

#Setting torch
mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
std = torch.Tensor([0.229, 0.224, 0.225]).cuda()
device = torch.device('cuda')

#parse and draw functions
parse_objects = ParseObjects(topology)
draw_objects = DrawObjects(topology)

#Setting up the camera. Check from jetcam librarby for USB camera 
camera = CSICamera(width=WIDTH, height=HEIGHT, capture_fps=30)
camera.running = True

#Images precrocess function
def preprocess(image):
    global device
    device = torch.device('cuda')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = PIL.Image.fromarray(image)
    image = transforms.functional.to_tensor(image).to(device)
    image.sub_(mean[:, None, None]).div_(std[:, None, None])
    return image[None, ...]

#Function to check necks and ankle positions on the image. This returns then if the person might be falling or has fallen

#Execute function
def execute(change):
    image = change['new']
    data = preprocess(image)
    cmap, paf = model_trt(data)
    cmap, paf = cmap.detach().cpu(), paf.detach().cpu()
    counts, objects, peaks = parse_objects(cmap, paf)
    draw_objects(image, counts, objects, peaks)
    processed = bgr8_to_jpeg(image[:, ::-1, :])
    return processed


#Start executing
cap = camera.value

while True:
    frame = execute (cap)
    cv2.imshow('human pose',frame)

    if cv2.waitKey(1) == 27:
        break


camera.unobserve_all()
camera.running = False