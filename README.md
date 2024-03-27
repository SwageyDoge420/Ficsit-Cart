# 1 Intro: A Fix it Cart

This repo contains the SW used to drive a fix it cart.


# 2 Hardware

A fix it cart__
A Rpi ZeroW__
A battery__
A servo__
A motor__
A battery charger/5V supply - 5V 2A Type-C USB 3.7V 18650 Lithium Li-ion Battery Charging Board DIY Power Bank__
A motor driver board - Dual H-Bridge Motor Driver 1.5A DC L298N__
A SD card__


# 3 RPI Software Install

https://www.raspberrypi.com/software/

Use the Raspberry PI disk imager to install the 32-bit Raspberry Pi OS Lite on an SD card. Make sure to get the lite version without a desktop.  Create a username ficsit and add a pass word.  Make sure to enable ssh and enter your wifi network and password.  When done eject and re-insert sd card.  

# 4 Connect to the Raspberry PI Zero over WiFi

From a terminal run the command below:  
ssh ficsit@raspberrypi.local  
If the host name could not be resolved you will have to use the IP address from your router.  


Update the pi:

sudo apt-get update && sudo apt-get upgrade -y

# 5 Pair the Bluetooth Controller

Most of these instructions came from here:
https://pimylifeup.com/xbox-controllers-raspberry-pi/

Install the Xbox drivers:
`sudo apt install xboxdrv`

Run this command to disable ERTM mode:
`echo 'options bluetooth disable_ertm=Y' | sudo tee -a /etc/modprobe.d/bluetooth.conf`

Reboot the pi:
`sudo reboot`

Re-login to the PI:
`ssh ficsit@raspberrypi.local`

Enter the follwoing commands to scan for bluetooth devices:
`sudo bluetoothctl`
`agent on`
`default-agent`

Turn on your Xbox controller and run the command below to start scanning for devices:
`scan on`

You should see a list of devices scrolling past.  Now press the pair button on the front of the XBOX controller.  Watch for an entry that looks like:
`[NEW] Device C8:3F:26:74:D5:57 Xbox Wireless Controller`

Once you see Xbox Controller enter the command below:
`scan off`

Then we can connect to the Xbox controller with the command, your ID might vary:
`pair C8:3F:26:74:D5:57`
`connect C8:3F:26:74:D5:57`

Then we make the device trusted so it will automatically connect to the RPI:
`trust C8:3F:26:74:D5:57`

We can now exit the bluetooth control software with the command:
`quit`

# 6 Install Software to Test the Controller

From test paired device:
https://raspberry-valley.azurewebsites.net/Map-Bluetooth-Controller-using-Python/
https://approxeng.github.io/approxeng.input/commandline.html`

sudo apt install python3-dev
sudo apt install python3-pip
sudo pip install evdev

Check your device is connected by running the command below:
`python3 /usr/local/lib/python3.9/dist-packages/evdev/evtest.py`


You should see something like:
`ID  Device               Name                                Phys                                Uniq
------------------------------------------------------------------------------------------------------------------  
0   /dev/input/event0    vc4-hdmi                            vc4-hdmi/input0                         
1   /dev/input/event1    Xbox Wireless Controller            b8:27:eb:33:b4:ce                   c8:3f:26:74:d5:57  `

Select the row number of the Xbox Controller.  Each button should produce information in the log file.  Control-C to quit.__

# Connect the Servo to the PI

Servo Wires:  
RED connect to +5V  
Brown connedt to GND  
Orange connect to GPIO_18 PWM  

Use the command below to see the pinout of the rpi:
`pinout`


# Install and test the Servo Software
This SW is used to control the steering servo.

https://pypi.org/project/rpi-hardware-pwm/

Follow the installation instructions for GPIO_18 and 19.

The code below should move the servo between thru its full range.  The min and max may need adjuted for your servo'.  If the servo is chattering the range is too high.  These numbers will take some fiddling.__
`from rpi_hardware_pwm import HardwarePWM

pwm = HardwarePWM(pwm_channel=0, hz=60, chip=0)
pwm.start(9) # Mid-point

pwm.change_duty_cycle(3.5)  # Minimum Point
pwm.change_duty_cycle(14.5)  # Maximum Point
pwm.stop()`


# Test the Motor GPIO

https://gpiozero.readthedocs.io/en/latest/index.html

Connect in+ to GPIO_23 pin 16
Connect in- to GPIO_24 pin 18


from gpiozero import Motor
from time import sleep

motor = Motor(forward=23, backward=24, pwm=True)
motor.forward(1.0)
motor.backward(0.1)
motor.forward(0.0)


# Connect the controller to the PI

import evdev

dev = evdev.InputDevice('/dev/input/event1')

print(dev)

dev.capabilities()

dev.capabilities(verbose=True)


# Test

Install git and download the software:
`sudo apt install git
git clone logan haglan fix it cart'

Code from here:
https://stackoverflow.com/questions/51564667/xbox-one-wireless-control-of-servo-using-analogue-stick-withevdev

Need to learn about event loops and crap.

With select:
https://github.com/gvalkov/python-evdev/issues/70
https://docs.python.org/3/library/select.html

asyncio looks like a good direction:
https://superfastpython.com/python-asyncio/


# Start the python on boot

Type to open the user chrontab:
`crontab -e`

Add teh line below to the opened file:
`@reboot /bin/sleep 5; /usr/bin/python /home/ficsit/ficsit/ficsit.py`
