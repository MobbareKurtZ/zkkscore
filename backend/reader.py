import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class Reader:
    reader = SimpleMFRC522()
    GPIO.setwarnings(False)
    read = True;

    def listen(self, timeout):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)
        try:
            timeout = time.time() + int(timeout)
            self.read = True;
            GPIO.output(7, GPIO.HIGH)
            while self.read:
                id = self.reader.read_id_no_block()
                time.sleep(0.1)
                if time.time() > timeout or not id == None:
                    break
        finally:
                GPIO.output(7, GPIO.LOW)
                GPIO.cleanup()
        return id

    def stop(self):
        self.read = False;
