# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LegoPyCar is a hobby robotics project combining a LEGO Technic car with Raspberry Pi Zero W, controlled via Xbox One wireless gamepad. The project demonstrates embedded systems programming with GPIO control, PWM, sensor integration, and real-time input handling.

**Hardware**: Raspberry Pi Zero W, Xbox One controller, N20-BT13 motor, TB6612FNG motor driver, SG-90 servo, HC-SR04 ultrasonic sensor, LEDs.

## Running the Application

```sh
cd LegoPyCar/
python3 main.py
```

The application must run on a Raspberry Pi with all hardware components connected. Exit the program by pressing the **Select button** on the Xbox controller.

## Xbox Controller Setup

The Xbox One controller connects via Bluetooth using Linux Joystick API (`/dev/input/js0`). Setup requires:

```sh
# Disable ERTM (Enhanced Re-Transmission Mode) - not well supported by Raspbian
echo 'options bluetooth disable_ertm=Y' | sudo tee -a /etc/modprobe.d/bluetooth.conf
sudo reboot

# Pair controller
sudo bluetoothctl
scan on
pair YOUR_MAC_ADDRESS
trust YOUR_MAC_ADDRESS
connect YOUR_MAC_ADDRESS

# Install Joystick API
sudo apt-get install joystick
```

## Architecture

The codebase follows a modular component-based design with single entry point:

```
main.py (entry point)
├── joy.py        - Xbox controller input via Linux Joystick API
├── engine.py     - Motor control (Engine class)
└── distance.py   - Ultrasonic sensor (ParkingDetector class)
```

### Module Responsibilities

**main.py** - Application controller and GPIO orchestration
- Initializes all GPIO pins and PWM instances
- Creates Engine, ParkingDetector, and Joystick objects
- Runs parking sensor in background daemon thread
- Main loop processes joystick input and routes to appropriate handlers
- Manages servo steering (X-axis), motor speed (triggers), and lights (A button)

**engine.py** - Motor control abstraction
- `Engine` class controls N20-BT13 motor via TB6612FNG driver
- Accepts flexible GPIO pin assignment via constructor
- Maps Xbox trigger input (-1 to 1 range) to PWM duty cycle (0-100%)
- Direction control: Z-axis trigger = forward, RZ-axis trigger = reverse
- PWM frequency configurable (default 200Hz)

**distance.py** - Parking detection system
- `ParkingDetector` class wraps HC-SR04 ultrasonic sensor
- `distance()` method returns distance in centimeters
- Timing-based measurement: sends 10μs trigger pulse, measures echo pulse duration
- Distance formula: (TimeElapsed × 34300cm/s) / 2

**joy.py** - Controller input handling
- Uses Linux Joystick API via `/dev/input/js0` device file
- Module executes initialization code at import time (opens device, reads capabilities)
- `Joystick.readJoystick()` returns tuple: (type, button/axis_name, value)
- Supports full Xbox One controller mapping including triggers, D-pad, buttons, analog sticks

### Control Flow

1. **Steering**: X-axis (left stick) → `getCycle()` → servo PWM calculation: `cycle = 5x + 7` (range 2%-12%)
2. **Motor**: Z/RZ triggers → `Engine.engineGo()` → direction + speed calculation → motor PWM
3. **Parking Sensor** (background thread):
   - Continuously polls distance sensor
   - 20-100cm: LED blinks faster as distance decreases (PWM frequency = 100/cm)
   - <20cm: LED solid, motor automatically brakes for 1 second
4. **Lights**: A button → `lights()` → toggles front LED state

## GPIO Pin Mapping

| Function | GPIO Pin | Type | PWM Frequency | Notes |
|----------|----------|------|---------------|-------|
| Servo (steering) | 18 | PWM OUT | 50Hz | SG-90 servo control |
| Parking LED | 12 | PWM OUT | Variable | Frequency modulated by distance |
| Motor Direction 1 | 4 | OUT | - | AIN1 on TB6612FNG |
| Motor Direction 2 | 17 | OUT | - | AIN2 on TB6612FNG |
| Motor Speed PWM | 21 | PWM OUT | 200Hz | PWMA on TB6612FNG |
| Motor Standby | 27 | OUT | - | STBY on TB6612FNG |
| Front Light Direction 1 | 5 | OUT | - | BIN1 on TB6612FNG |
| Front Light Direction 2 | 6 | OUT | - | BIN2 on TB6612FNG |
| Front Light PWM | 2 | PWM OUT | - | PWMB on TB6612FNG |
| Distance Trigger | 13 | OUT | - | HC-SR04 trigger pulse |
| Distance Echo | 19 | IN | - | HC-SR04 echo timing |

All GPIO operations use BCM pin numbering (`GPIO.setmode(GPIO.BCM)`).

## Important Implementation Notes

**Module-level code execution**: `joy.py` executes initialization code when imported (opens `/dev/input/js0`, performs ioctl calls). This means importing the module has side effects. Controller must be connected before running `main.py`.

**Threading**: The parking sensor runs in a daemon thread, automatically terminated when main loop exits. This ensures continuous distance monitoring without blocking controller input.

**PWM instances**: Multiple PWM instances are created in main.py for servo, parking LED, and motor. Engine class also creates its own PWM instance for motor speed control.

**Servo calibration**: The formula `cycle = 5x + 7` is calibration-specific to the SG-90 servo used. 2% duty cycle = -90°, 12% duty cycle = +90°. Different servos may require recalibration.

**Motor braking**: When obstacle detected <20cm, parking sensor thread calls `motor.engineOff()` then `motor.engineOn()` with 1-second delays. This creates a brake effect but may interfere with manual control.

**GPIO cleanup**: The try-finally block in main loop ensures `GPIO.cleanup()` is called on exit, but PWM stop methods are called without parentheses (`pwm.stop` instead of `pwm.stop()`), which means they don't execute properly.

## Code Style

- No type hints or docstrings (except one docstring in `getCycle()`)
- Minimal error handling
- BCM GPIO numbering mode
- Class constructors accept GPIO pins for flexibility
- No configuration files - all settings hardcoded in main.py
