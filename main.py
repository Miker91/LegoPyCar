import joy
import engine
import distance
import RPi.GPIO as GPIO
import threading
from time import sleep

# ---------GPIO Handling----------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_SERVO_PIN  = 18
GPIO_BUZZER = 12
GPIO.setup(GPIO_SERVO_PIN, GPIO.OUT)
GPIO.setup(GPIO_BUZZER, GPIO.OUT)

# SET PWM Servo
pwm = GPIO.PWM(GPIO_SERVO_PIN,50)
pwm.start(0)

# SET PWM LED - Parking detector
pwmParking = GPIO.PWM(GPIO_BUZZER,0.5)
pwmParking.start(0)


# Set xBox controller
xbox = joy.Joystick()
# Set engine
motor = engine.Engine()

def getCycle(axis, x):
    """Calculate pulse for PWM and move servo.
    My srvo worked quite different than stated in documentation, so after some testing it came out that:
    2% is -90deg
    12% is 90deg
    calculation has been done simply using f(x)=5x+7
    """
    if axis == "x":
        cycle = 5*x+7
        pwm.ChangeDutyCycle(cycle)
    # check if pad triggers were used
    elif axis == "z" or axis == "rz":
        motor.engineGo(axis, x)
    else:
        pass

def parkingSensor():    
    while True:
        cm = distance.distance()
        if cm < 100 and cm >= 20:
            pwmParking.ChangeFrequency(100/cm)
            pwmParking.ChangeDutyCycle(50)
        elif cm < 20:
            pwmParking.ChangeDutyCycle(100)
            # Brake to avoid collision
            motor.engineOff()
            sleep(1)
            motor.engineOn()
            sleep(1)
        else:
            pwmParking.ChangeDutyCycle(0)
        sleep(0.5)

#main loop
if __name__ == "__main__":
    # Run a loop in a separate thread.
    t1 = threading.Thread(target=parkingSensor)
    # Daemon will make sure that interrupting of main loop will also kill a thread
    t1.daemon = True
    t1.start()
    try:
        while True:
            type, button, state = xbox.readJoystick()
            # print(type, button, state)
            if type == "button":
                # button pressed
                if state:
                    if button == "select":
                        break
                else:
                    # The place for further buttons assignments
                    pass
            elif type == "axis":
                    getCycle(button, state)
    finally:
        # Clean-up
        print("Cleaning GPIO")
        pwm.start(0)
        pwm.stop
        pwmParking.stop
        GPIO.cleanup()

