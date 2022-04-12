import jetson.utils
import jetson.inference
import settings
import sys

camera = jetson.utils.videoSource(settings.camera, settings.camera_argv)
output = jetson.utils.videoOutput(settings.output, settings.output_argv)
net = jetson.inference.poseNet("resnet18_baseline_att_224x224_A_epoch_249_trt.pth", sys.argv, "0.5")

while True:
    # capture the next image
    img = input.Capture()

    # perform pose estimation (with overlay)
    poses = net.Process(img, overlay="links, keypoints")

    # render the image
    output.Render(img)

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break