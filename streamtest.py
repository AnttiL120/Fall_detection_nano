import jetson.inference
import jetson.utils
import sys
import settings

# load the pose estimation model
net = jetson.inference.poseNet("resnet18_baseline_att_224x2245_A_epoch_249_trt.pth", sys.argv, 0.5)
# create video sources & outputs
input = jetson.utils.videoSource(settings.camera, settings.camera_argv)
output = jetson.utils.videoOutput(settings.output, settings.output_argv)

# process frames until the user exits
while True:
    # capture the next image
    img = input.Capture()

    # perform pose estimation (with overlay)
    poses = net.Process(img, overlay="links,keypoints")

    # print the pose results
    print("detected {:d} objects in image".format(len(poses)))

    for pose in poses:
        print(pose)
        print(pose.Keypoints)
        print('Links', pose.Links)

    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format("resnet18-body", net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break