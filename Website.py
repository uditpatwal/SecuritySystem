import threading
import argparse
import datetime
import imutils
import time
import cv2
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template

class Website:
    
    global app

    def __init__(self):
        self.outputFrame = None
        self.name = "No one"
        # lock = threading.Lock()
        # Initialize our Flaskapp
        self.app = Flask(__name__)

        def generate():
            while True:
                # check if the output frame is available, otherwise skip
                # the iteration of the loop
                if self.outputFrame is None:
                    print("shittt")
                    continue
                # encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", self.outputFrame)
                # ensure the frame was successfully encoded
                if not flag:
                    continue
                # print("shitttt")
                # yield the output frame in the byte format
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n"
                    + bytearray(encodedImage)
                    + b"\r\n"
                )

        def generateName():
            while True:
                yield (self.name)

        @self.app.route("/video_feed")
        def video_feed():
            # return the response generated along with the specific media
            # type (mime type)
            return Response(
                generate(), mimetype="multipart/x-mixed-replace; boundary=frame"
            )

        @self.app.route("/")
        def home():
            return render_template("index.html", content="what are you doing here?")

        @self.app.route("/pepperoni")
        def pepperoni():
            return "Hello! Here are some nice pepperonis!"

        @self.app.route("/video/")
        def video():
            return render_template("video.html")

    def recieveOutputFrame(self, rec):
        self.outputFrame = rec

    def recieveName(self, name):
        self.name = name
