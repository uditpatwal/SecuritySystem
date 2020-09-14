import threading
import argparse
import datetime
import imutils
import time
import cv2
import flask_login
from config import Config
from imutils.video import VideoStream
from flask import Response, Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class Website:

    global app
    users = {"udit@patwal.com": {"password": "secret"}}

    def __init__(self):
        self.outputFrame = None
        self.name = "No one"
        # lock = threading.Lock()

        # Initialize our Flaskapp
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        # Initialize login manager for individual users
        self.login_manager = flask_login.LoginManager()
        self.login_manager.init_app(self.app)

        class User(flask_login.UserMixin):
            pass

        @self.login_manager.user_loader
        def user_loader(email):
            if email not in self.users:
                return

            user = User()

            user.id = email
            return user

        @self.login_manager.request_loader
        def request_loader(request):
            email = request.form.get("email")
            if email not in self.users:
                return

            user = User()
            user.id = email

            user.is_authenticated = (
                request.form["password"] == self.users[email]["password"]
            )

            return user

        @self.login_manager.unauthorized_handler
        def unauthorized_handler():
            flash("You cannot access Videos until logged in")
            return redirect(url_for("home"))

        def generate():
            while True:
                # check if the output frame is available, otherwise skip
                # the iteration of the loop
                if self.outputFrame is None:
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
        @flask_login.login_required
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
        @self.app.route("/login", methods=["GET", "POST"])
        def login():
            form = LoginForm()
            if form.validate_on_submit():
                flash(
                    "Login requested for user {}, remember_me={}".format(
                        form.username.data, form.remember_me.data
                    )
                )
                if form.username.data not in self.users:
                    flash("Invalid username or password")
                    return redirect(url_for("login"))
                elif form.password.data == self.users[form.username.data]["password"]:
                    user = User()
                    user.id = form.username.data
                    flask_login.login_user(user)
                    return redirect("/")
                else:
                    flash("Invalid username or password")
                    return redirect(url_for("login"))
            return render_template("login.html", title="Sign In", form=form)

        @self.app.route("/pepperoni")
        def pepperoni():
            return "Hello! Here are some nice pepperonis!"

        @self.app.route("/video")
        @flask_login.login_required
        def video():
            return render_template("video.html")

    def recieveOutputFrame(self, rec):
        self.outputFrame = rec

    def recieveName(self, name):
        self.name = name
