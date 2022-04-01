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

with open('human_pose.json', 'r') as f:
    human_pose = json.load(f)

topology = trt_pose.coco.coco_category_to_topology(human_pose)

WIDTH = 224
HEIGHT = 224
data = torch.zeros((1, 3, HEIGHT, WIDTH)).cuda()
OPTIMIZED_MODEL = 'resnet18_baseline_att_224x224_A_epoch_249_trt.pth'

model_trt = TRTModule()
model_trt.load_state_dict(torch.load(OPTIMIZED_MODEL))

topology = trt_pose.coco.coco_category_to_topology(human_pose)
mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
std = torch.Tensor([0.229, 0.224, 0.225]).cuda()
device = torch.device('cuda')

parse_objects = ParseObjects(topology)
draw_objects = DrawObjects(topology)
camera = CSICamera(width=WIDTH, height=HEIGHT, capture_fps=30)


def preprocess(image):
    global device
    device = torch.device('cuda')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = PIL.Image.fromarray(image)
    image = transforms.functional.to_tensor(image).to(device)
    image.sub_(mean[:, None, None]).div_(std[:, None, None])
    return image[None, ...]

def check_pose(objects, normalized_peaks):

    i = 18
    neck = 6
    neck_posx = []
    neck_posy = []
    left_ankle = 7
    left_ankle_posx = []
    left_ankle_posy = []
    right_ankle= 12
    right_ankle_posx = []
    right_ankle_posy = []
    height = 224
    width = 224
    fall_value = 20
    pose_position = 0

    obj = objects[0][i]
    C = obj.shape[0]
    for j in range(C):
        k = int(obj[j])
        if k >= 0:
            peak = normalized_peaks[0][j][k]
            x = round(float(peak[1]) * width)
            y = round(float(peak[0]) * height)
            if j == neck:
                neck_posx = x
                neck_posy = y
            if j == left_ankle:
                left_ankle_posx = x
                left_ankle_posy = y
            if j == right_ankle:
                right_ankle_posx = x
                right_ankle_posy = y
        else:
            pose_position = 0

    if neck_posy - left_ankle_posy < fall_value:
        pose_position = -1
    
    elif neck_posy - right_ankle_posy < fall_value:
        pose_position = -1

    elif neck_posx - left_ankle_posx < fall_value or neck_posx - right_ankle_posx < fall_value:
        pose_position = 2

    else:
        pose_position = 1

    print(pose_position)
    return pose_position

def execute(change):
    image = change['new']
    data = preprocess(image)
    cmap, paf = model_trt(data)
    cmap, paf = cmap.detach().cpu(), paf.detach().cpu()
    counts, objects, peaks = parse_objects(cmap, paf)
    current_pose = check_pose(objects, peaks)
    if current_pose == 2:
        color = (0, 255, 0)
    elif current_pose == 1:
        color = (255, 255, 0)
    elif current_pose == -1:
        color = (0, 0, 255)
    else:
        color = (255, 255, 255)
    
    draw_objects(image, counts, objects, peaks, color)
    processed_image = bgr8_to_jpeg(image[:, ::-1, :])

    return processed_image

execute({'new': camera.value})
camera.observe(execute, names='value')