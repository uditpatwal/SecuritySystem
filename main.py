import threading
import argparse
import datetime
import imutils
import time
import cv2
import RPi.GPIO as GPIO
from LockMechanism import Lock
from Website import Website
from face_test import Recognizer
from database import Database


def camera(frame_count):

    global vs, outputFrame, processFrame, count, name, unlockTimer, initTimer, changeLockState
    try:
        while True:
            ret, frame = vs.read()
            # frame = imutils.resize(frame, width=400)
            recognizer.run(frame)
            outputFrame = recognizer.getOutputFrame()
            temp = recognizer.getDetectedFaceTimes()
            foundUnlocker = False
            for t in temp:
                print(str(temp[t][0]) + ", " + str(temp[t][1]) + ", " + str(temp[t][2]))

                # FIX ME: POTENTIAL BUG HERE
                if not temp[t][2]:
                    time_start_obj = datetime.datetime.strptime(
                        temp[t][0], "%Y-%m-%d %H:%M:%S"
                    )
                    time_stop_obj = datetime.datetime.strptime(
                        temp[t][1], "%Y-%m-%d %H:%M:%S"
                    )
                    time_elapsed = time_stop_obj - time_start_obj
                    database.addPersonTime(
                        t, temp[t][0], str(time_elapsed.total_seconds())
                    )
                else:
                    time_start_obj = datetime.datetime.strptime(
                        temp[t][0], "%Y-%m-%d %H:%M:%S"
                    )
                    time_now_obj = datetime.datetime.now()
                    time_elapsed = time_now_obj - time_start_obj

                    if time_elapsed.total_seconds() > 3:
                        print(time_elapsed.total_seconds())
                        foundUnlocker = True
            if foundUnlocker and not unlockTimer.is_alive() and initTimer:
                doorLock.unlock()
                unlockTimer.start()
                initTimer = False
                database.addPersonToUnlock(t, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True)
            elif not unlockTimer.is_alive() and not initTimer:
                unlockTimer = threading.Timer(5.0, doorLock.lock)
                initTimer = True

            name = recognizer.getName()
            web.recieveName(name)
            web.recieveOutputFrame(outputFrame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
            timestamp = datetime.datetime.now()
            cv2.putText(
                frame,
                timestamp.strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (0, 0, 255),
                1,
            )
    except KeyboardInterrupt:
        print("Exited the program")

    except Exception as e:

        print("Some stupid error occured " + str(e))

    finally:
        print("STOPPING LOCK")
        doorLock.stop()


outputFrame = None
lock = threading.Lock()
vs = cv2.VideoCapture(0)
time.sleep(0.5)
doorLock = Lock()
shouldLock = True
web = Website()
recognizer = Recognizer()
database = Database()
processFrame = False
count = 0
name = "No one"
changeLockState = False
initTimer = True
unlockTimer = threading.Timer(5.0, doorLock.lock)

# Checks to see if this is the main thread of execution
if __name__ == "__main__":
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-i", "--ip", type=str, required=True, help="ip address of the device"
    )
    ap.add_argument(
        "-o",
        "--port",
        type=int,
        required=True,
        help="ephemeral port number of the server (1024 to 65535)",
    )
    ap.add_argument(
        "-f",
        "--frame-count",
        type=int,
        default=60,
        help="# of frames used to construct the background model",
    )
    args = vars(ap.parse_args())
    # start a thread that will perform motion detection
    t = threading.Thread(target=camera, args=(args["frame_count"],))
    t.daemon = True
    t.start()
    # start the flask app
    web.app.run(
        host=args["ip"],
        port=args["port"],
        debug=True,
        threaded=True,
        use_reloader=False,
    )
