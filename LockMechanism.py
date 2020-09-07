from  gpiozero import servo
from time import sleep

class Lock:
    
# servo.min() will be the LOCKING position of the servo.
# There will be a set position 90 degrees away from min that will be unlocked.

    def __init__(self):
        # Setting the servo to GPIO PIN 18
        servo = Servo(18)

    def lock(self):
        # lock the lock
        servo.min()
    
    def unlock(self):
        #unlock the lock
        servo.mid()
    

    
    
