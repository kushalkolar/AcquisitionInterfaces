from camera_interfaces import OpenCVCameraGrabber
from writers import TiffWriter
import time

frame_grabber = OpenCVCameraGrabber(10, (960, 540), 0.05, 10, 0)

writer = TiffWriter(frame_grabber.queue, None, '/home/kushal/test_acq_writer_bah.tiff', 2, preview=True)

frame_grabber.start()
writer.start()
