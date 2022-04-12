import jetson.inference
import jetson.utils
import json
import trt_pose.coco
import torch
from torch2trt import TRTModule
import cv2
import torchvision.transforms as transforms
import PIL.Image
from draw import DrawObjects
from trt_pose.parse_objects import ParseObjects

#Topology for human pose
with open('human_pose.json', 'r') as f:
    human_pose = json.load(f)

topology = trt_pose.coco.coco_category_to_topology(human_pose)

#Resolution on the model was 224x224 so using the same resolution
WIDTH = 1280
HEIGHT = 720
FPS = 30
data = torch.zeros((1, 3, HEIGHT, WIDTH)).cuda()

#Load optimizied model
OPTIMIZED_MODEL = 'resnet18_baseline_att_224x224_A_epoch_249_trt.pth'
model_trt = TRTModule()
model_trt.load_state_dict(torch.load(OPTIMIZED_MODEL))

#Setting torch ready
mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
std = torch.Tensor([0.229, 0.224, 0.225]).cuda()
device = torch.device('cuda')

#parse and draw functions
parse_objects = ParseObjects(topology)
draw_objects = DrawObjects(topology)

#Images precrocess function
def preprocess(image):
    global device
    device = torch.device('cuda')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = PIL.Image.fromarray(image)
    image = transforms.functional.to_tensor(image).to(device)
    image.sub_(mean[:, None, None]).div_(std[:, None, None])
    return image[None, ...]

#Execute function
def execute(image):
    data = preprocess(image)
    cmap, paf = model_trt(data)
    cmap, paf = cmap.detach().cpu(), paf.detach().cpu()
    counts, objects, peaks = parse_objects(cmap, paf)
    draw_objects(image, counts, objects, peaks)


camera = jetson.utils.videoSource("csi://0", argv=['--input-width=1280', '--input-height=720', '--input-flip=FLIP'])
display = jetson.utils.videoOutput("rtp://192.168.1.44:1234",argv=["--bitrate=10000000", "--headless"])

while True:
    img = camera.Capture()

    img = preprocess(img)

    display.Render(img)
    if not camera.IsStreaming() or not display.IsStreaming():
        break
