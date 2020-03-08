import joy
import engine
import distance
import RPi.GPIO as GPIO
import threading
from time import sleep

# ---------GPIO Handling----------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Servo PWM GPIO
GPIO_SERVO_PIN  = 18

#LED GPIO for parking detecotor
GPIO_LED = 12

#Motor GPIOs
GPIO_AIN1 = 4
GPIO_AIN2 = 17
GPIO_PWMA = 21
GPIO_STBY = 27
MOTOR_PWM_HZ = 200

#Distance detector GPIOs
GPIO_TRIGGER = 13
GPIO_ECHO = 19

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_SERVO_PIN, GPIO.OUT)
GPIO.setup(GPIO_LED, GPIO.OUT)

# SET PWM Servo
pwm = GPIO.PWM(GPIO_SERVO_PIN,50)
pwm.start(0)

# SET LED PWM- Parking detector
pwmParking = GPIO.PWM(GPIO_LED,0.5)
pwmParking.start(0)
# ---------GPIO Handling----------

# Create objects for parking detector, controller, and motor engine 
# Set parking (distacne) detector and assign GPIOs
detector = distance.ParkingDetector(GPIO_TRIGGER,GPIO_ECHO)
# Set xBox controller
xbox = joy.Joystick()
# Set engine and assign GPIOs and Hz
motor = engine.Engine(GPIO_AIN1,GPIO_AIN2,GPIO_PWMA,GPIO_STBY,MOTOR_PWM_HZ)

def getCycle(axis, x):
    """Calculate pulse for PWM and move servo.
    My servo worked quite different than stated in documentation, so after some testing it came out that:
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
        cm = detector.distance()
        if cm < 100 and cm >= 20:
            "Controll LED blinking frequency"
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
        sleep(0.1)

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

