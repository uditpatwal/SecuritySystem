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

# Method that continuously runs the door locking program
def system():

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
                # This records how long the person was detected for
                if not temp[t][2]:
                    time_start_obj = temp[t][0]     
                    time_stop_obj = temp[t][1]
                    time_elapsed = time_stop_obj - time_start_obj
                    database.addPersonTime(
                        t, temp[t][0], str(time_elapsed.total_seconds())
                    )
                # Checks how long a current person is being detected for then opens door after specified time
                else:
                    time_start_obj = temp[t][0]
                    time_now_obj = datetime.datetime.now()
                    time_elapsed = time_now_obj - time_start_obj

                    if time_elapsed.total_seconds() > 3:
                        print(time_elapsed.total_seconds())
                        foundUnlocker = True


            # TODO: Add Admin Override 

            # Door Locking Mechanics
            if foundUnlocker and not unlockTimer.is_alive() and initTimer:
                doorLock.unlock()
                unlockTimer.start()
                initTimer = False
                database.addPersonToUnlock(
                    t, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True
                )
            elif not unlockTimer.is_alive() and not initTimer:
                unlockTimer = threading.Timer(5.0, doorLock.lock)
                initTimer = True

            name = recognizer.getName()
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
# start a thread that will perform motion detection
t = threading.Thread(target = system)
t.daemon = True
t.start()
# start the flask app
web.app.run(
    host = '192.168.1.7',
    port= '5000',
    debug=True,
    threaded=True,
    use_reloader=False,
)

