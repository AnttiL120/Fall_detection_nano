from jetcam.csi_camera import CSICamera

WIDTH = 224
HEIGHT = 224

camera = CSICamera(width=WIDTH, height=HEIGHT, capture_fps=30)
camera.unobserve_all()
camera.running = False