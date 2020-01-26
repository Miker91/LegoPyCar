import RPi.GPIO as GPIO
from time import sleep


last_axis_used = ""

GPIO_AIN1 = 4
GPIO_AIN2 = 17
GPIO_PWMA = 21
GPIO_STBY = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_AIN1, GPIO.OUT)
GPIO.setup(GPIO_AIN2, GPIO.OUT)
GPIO.setup(GPIO_STBY, GPIO.OUT)
GPIO.setup(GPIO_PWMA, GPIO.OUT)
pwm = GPIO.PWM(GPIO_PWMA,200)


print("MOLdul zainportowany")

class Engine(object):
    """docstring for Engine."""
    def __init__(self):
        self.engineOn()

    def engineOn(self):
        GPIO.output(GPIO_STBY,GPIO.HIGH)
        pwm.start(0)

    def engineOff(self):
        GPIO.output(GPIO_STBY,GPIO.LOW)

    def engineGo(self, axis, btn):
    # """This function will calculate direction and speed of engine concidering usage of both pad trriggers.
    # The range will be from -1(full back) to 1(full forvard)"""

        print(axis, last_axis_used)
        direction = self.engineDirection(axis, btn)
        print(direction)
        speed = self.engineSpeed(btn)
        print ("Motor cycle is: ", speed)
        pwm.ChangeDutyCycle(speed)

    def engineDirection(self, axis, btn):
        if axis == "z" and btn != -1:
            GPIO.output(GPIO_AIN1,GPIO.HIGH)
            return 1
        elif axis == "rz" and btn != -1:
            GPIO.output(GPIO_AIN2,GPIO.HIGH)
            return -1
        elif axis == "z" and btn == -1:
            GPIO.output(GPIO_AIN1,GPIO.LOW)
            return 0
        elif axis == "rz" and btn == -1:
            GPIO.output(GPIO_AIN2,GPIO.LOW)
            return 0

    def engineSpeed(self, btn):
        """ Calculates PWM based on triggers level"""
        return (btn + 1)/2 * 100
