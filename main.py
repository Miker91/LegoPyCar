import joy
import engine
import distance
import RPi.GPIO as GPIO
import threading
from time import sleep
# Set xBox 
xbox = joy.Joystick()

# GPIO handling
# https://tutorials-raspberrypi.com/raspberry-pi-xbox-360-controller-wireless/
# ----------------------------------------------------

# Only one engine is needed
# GPIO CONSTs SERVO
GPIO_SERVO_PIN  = 18
GPIO_BUZZER = 12
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(GPIO_SERVO_PIN, GPIO.OUT)
GPIO.setup(GPIO_BUZZER, GPIO.OUT)

# Set engine
motor = engine.Engine()

def getCycle(axis, x):
    """Calculate pulse for pwm and move servo
    my srvo worked unexpectly, so after some testing it came out that
    2% is -90deg
    12% is 90deg
    it has been done using f(x)=5x+7
    """
    if axis == "x":
        # if x == 0:
        #     ms = x + 1.5
        #     # cycle = (ms/20)*100
        # else:
        cycle = 5*x+7
            # ms = x/2 +1.5
            # cycle = (ms/20)*100
        moveServo(cycle)
    # check if pad triggers were used
    elif axis == "z" or axis == "rz":
        motor.engineGo(axis, x)
    else:
        pass

def moveServo(cycle):
    # sleep(0.1)
    print(cycle)
    pwm.ChangeDutyCycle(cycle)


def stopServo():
    pwm.stop

#SET PWM Servo
pwm = GPIO.PWM(GPIO_SERVO_PIN,50)
pwm.start(0)

#SET PWM Buzzer
pwmParking = GPIO.PWM(GPIO_BUZZER,0.5)
pwmParking.start(0)

#main loop
def parkingSensor():
    #enable buzzer
    
    run = True
    while run:
        cm = distance.distance()
        if cm < 100 and cm >= 10:
            print("PWM", 10/cm*100)
            pwmParking.ChangeDutyCycle(10/cm*100)
        elif cm < 10:
            pwmParking.ChangeDutyCycle(100)
            motor.engineOff()
        else:
            pwmParking.ChangeDutyCycle(0)
        sleep(0.5)


if __name__ == "__main__":
#    t1 = threading.Thread(target=parkingSensor)
#    t1.daemon = True
#    t1.start()
    try:
        while True:
            type, button, state = xbox.readJoystick()
            print(type, button, state)
            if type == "button":
                # button pressed
                if state:
                    if button == "select":
                        break
                else:
                    pass
            elif type == "axis":
                    getCycle(button, state)
    finally:
        # Clean-up
        pwm.start(0)
        pwm.stop
        pwmParking.stop
        GPIO.cleanup()

