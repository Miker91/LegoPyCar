import joy
import engine
import RPi.GPIO as GPIO

# Set xBox controller and engine
xbox = joy.Joystick()

# GPIO handling
# https://tutorials-raspberrypi.com/raspberry-pi-xbox-360-controller-wireless/
# ----------------------------------------------------
# VCC	zasilanie części logicznej
#  VMOT	zasilanie silników
#  GND	masa
# AO1 AO2	wyjścia kanału A
# BO1 BO2	wyjścia kanału B
# PWMA	sygnał PWM kanału A
# PWMB	sygnał PWM kanału B
# STBY	należy podciągnąć do VCC aby włączyć układ, stan niski (domyślny) przełącza układ w stan uśpienia (niskiego poboru mocy)
# AIN1, AIN2	sterowanie kierunkiem kanału A
# BIN1, BIN2	sterowanie kierunkiem kanału B

# Only one engine is needed
# GPIO CONSTs SERVO
GPIO_SERVO_PIN  = 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(GPIO_SERVO_PIN, GPIO.OUT)

motor = engine.Engine()

def getCycle(axis, x):
    """Calculate pulse for pwm and move servo
    my srvo worked unexpectly, so after some testing it came out that
    2% is -90%
    12% is 90%
    it has been done using f(x)=5x+7
    """
    if axis == "x":
        if x == 0:
            ms = x + 1.5
            cycle = (ms/20)*100
        else:
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

#SET PWM
pwm = GPIO.PWM(GPIO_SERVO_PIN,50)
pwm.start(0)

#main loop
if __name__ == "__main__":
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
        GPIO.cleanup()
        pwm.start(0)
        pwm.stop
