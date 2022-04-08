import jetson.inference
import jetson.utils
import argparse
import sys
import json
import trt_pose.coco
import torch
from torch2trt import TRTModule
import cv2
import torchvision.transforms as transforms
import PIL.Image
from draw import DrawObjects
from trt_pose.parse_objects import ParseObjects

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

#Topology for human pose
with open('human_pose.json', 'r') as f:
    human_pose = json.load(f)

topology = trt_pose.coco.coco_category_to_topology(human_pose)

#Resolution on the model was 224x224 so using the same resolution
WIDTH = 224
HEIGHT = 224
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


# create video output object 
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)
# create video sources
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)

# process frames until the user exits
while True:
	# capture the next image
	img = input.Capture()

	execute(img)
	
	# render the image
	output.Render(img)

	# exit on input/output EOS
	if not input.IsStreaming() or not output.IsStreaming():
		break
