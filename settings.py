network = "restnet18_baseline_att_224x224_A_epoch_249_trt.pth"
network_argv = argv=['--model=restnet18_baseline_att_224x224_A_epoch_249_trt.pth']

camera = "csi://0"
camera_argv = argv=['--input-width=224', '--input-height=224']

output = "rtp://192.168.1.44:1234"
output_argv = argv=['--bitrate=10000000', '--headless']