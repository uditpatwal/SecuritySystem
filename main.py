import threading
import argparse
import datetime
import imutils
import time
import cv2
from Website import Website
from face_test import Recognizer


def camera(frame_count):
    
    global vs, outputFrame, processFrame, count, name
    
    while True:
        ret, frame = vs.read()
        #frame = imutils.resize(frame, width=400)
        recognizer.run(frame)
        outputFrame = recognizer.getOutputFrame()
        name = recognizer.getName()
        web.recieveName(name)
        web.recieveOutputFrame(outputFrame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

outputFrame = None
lock = threading.Lock()
vs = cv2.VideoCapture(0)
time.sleep(0.5)
web = Website()
recognizer = Recognizer()
processFrame = False
count = 0
name = "No one"
time.sleep(0.5)
# Checks to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
        help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
        help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=60,
        help="# of frames used to construct the background model")
    args = vars(ap.parse_args())
    # start a thread that will perform motion detection
    t = threading.Thread(target=camera, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()
    # start the flask app
    web.app.run(host=args["ip"], port=args["port"], debug=True,
        threaded=True, use_reloader=False)



