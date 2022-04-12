import jetson.utils

camera = jetson.utils.videoSource("csi://0", argv=['--input-width=1280', '--input-height=720', '--input-flip=rotate-180'])
display = jetson.utils.videoOutput("rtp://192.168.1.44:1234",argv=["--bitrate=10000000", "--headless"])

while True:
    img = camera.Capture()
    display.Render(img)
    if not camera.IsStreaming() or not display.IsStreaming():
        break