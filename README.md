<p align="center">
  <a href="" rel="noopener">
 <img width=300px height=200px src="https://i.imgur.com/uckoFtX.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Lego PyCar</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---


## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Build your CAR!](#build)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

The short genesis of the project: 2 years ago for my b-day I received Xbox one pad, this year (also b-day gift) I got Lego car and on Christmas- Raspberry Pi Zero W. 
So I decided to use all those gits, get some knowledge of electronics and create my first project. 

<a href="https://imgur.com/uckoFtX"><img src="https://i.imgur.com/uckoFtX.jpg?1" title="source: imgur.com" /></a>

Short video:

[![Lego PyCar](https://img.youtube.com/vi/Ob1t2S5xnmg/0.jpg)](https://www.youtube.com/watch?v=Ob1t2S5xnmg)

## 🏁 Getting Started <a name = "getting_started"></a>

### Prerequisites

- Raspberry PI Zero W
- Xbox one pad
- Motor: N20-BT13
- TB6612FNG Dual Motor Driver Carrier 
- Servo SG-90
- hc-sr04 distance sensor + holder
- LEGO - Technic First Responder (or any other)
- Power bank, 
- 9v Battery,
- LED or buzzer,
- resistors (2x330 and 480 Ω) 
- Cables and soldering iron


### Installing

1.	Connecting Xbox pad to Raspberry
This task is relatively easy as our PI Zero W have build in Bluetooth module, and new Xbox controller doesn’t require additional adapters. Unfortunately there is also one disadvantage, but about that, later on. Connection can be done with following commands in terminal:
```sh
echo 'options bluetooth disable_ertm=Y' | sudo tee -a /etc/modprobe.d/bluetooth.conf
```
ertn (Enhanced Re-Transmission Mode) is not well supported by Raspbian and can cause connection interuptions.
Restart:
```sh
sudo reboot
```
Open Bluetooth agent and scan devices.
```sh
sudo bluetoothctl
scan on
```
All available devices will pop up on a list, you should be able to find your controller and check it’s MAC address. Then:
```sh
pair YOUR_MAC_ADDRESS
trust YOUR_MAC_ADDRESS
connect YOUR_MAC_ADDRESS
```
For communication between pad and Raspberry I used Joystick API. I know, there is xboxdrv available for Python, which works well, but it doesn’t support bard new Xbox controller 😊. 
So, let’s install this API:
```sh
sudo apt-get install joystick
```
And clone repository.

git clone https://github.com/Miker91/LegoPyCar

## 🔧 Build you CAR!!! <a name = "build"></a>

I know that attached schemas are tragic, but this is my first shoot. They will help you assemble the model.
Fitting everything in such a small model is not a simple task but I'm sure you will manage :)

<a href="https://imgur.com/BQzUUik"><img src="https://i.imgur.com/BQzUUik.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/CBF8opD"><img src="https://i.imgur.com/CBF8opD.png" title="source: imgur.com" /></a>

Some build tips:

- How servo works?

[![Lego PyCar - Servo](https://img.youtube.com/vi/OvUSUD9pb9Q/0.jpg)](https://www.youtube.com/watch?v=OvUSUD9pb9Q)

- How motor works?

[![Lego PyCar - Motor](https://img.youtube.com/vi/aciQOdVaWjI/0.jpg)](https://www.youtube.com/watch?v=aciQOdVaWjI)


## 🎈 Usage <a name="usage"></a>

Application can by run by:
```sh
cd LegoPyCar/
python3 main.py
```

## ✍️ Authors <a name = "authors"></a>

- [@Miker91](https://github.com/Miker91) - Idea & Initial work

See also the list of [contributors](https://github.com/Miker91/LegoPyCar/graphs/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- References: https://gist.github.com/rdb/8864666 great code for use Joystick API

