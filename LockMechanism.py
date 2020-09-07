import RPi.GPIO as GPIO
import time

class Lock:
    
# servo.min() will be the LOCKING position of the servo.
# There will be a set position 90 degrees away from min that will be unlocked.

    def __init__(self):
        # Setting the servo to GPIO PIN 18
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        self.servo = GPIO.PWM(11, 50)
        self.servo.start(0)

    def lock(self):
        # lock the lock
        self.servo.ChangeDutyCycle(7)
    
    def unlock(self):
        #unlock the lock
        self.servo.ChangeDutyCycle(2)
        
    def stop(self):
        self.servo.stop()
        GPIO.cleanup()
        

   
    
