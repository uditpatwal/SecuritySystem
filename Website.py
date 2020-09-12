import threading
import argparse
import datetime
import imutils
import time
import cv2
import flask-login
from imutils.video import VideoStream
from flask import Response, Flask, render_template, redirect, url_for, request

class Website:
    
    global app

    def __init__(self):
        self.outputFrame = None
        self.name = "No one"
        # lock = threading.Lock()
        # Initialize our Flaskapp
        self.login_manager = LoginManager()
        self.app = Flask(__name__)
        self.login_manager.init_app(app)


        


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

        # Route for handling the login page logic
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            error = None
            if request.method == 'POST':
                if request.form['username'] != 'admin' or request.form['password'] != 'admin':
                    error = 'Invalid Credentials. Please try again.'
                else:
                    return redirect(url_for('home'))
            return render_template('login2.html', error=error)

        
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
