# File to run the ficsit car.  This takes teh xbox controller commands and
# converts them to GPIO commands on teh raspberry PI

import time
import evdev
from evdev import InputDevice, categorize, ecodes
from rpi_hardware_pwm import HardwarePWM
from gpiozero import Motor, LED

CENTER_TOLERANCE = 350
STICK_MAX = 65536

# Steering Servo
min = 7.8
max = 11.7


mid = (14.5 + 3.5) / 2.0
range = (14.5 - 3.5) / 2.0


pwm = HardwarePWM(pwm_channel=0, hz=60, chip=0)
pwm.start(mid) # Mid-point


# Drive Motor
fwd = 0.0
rev = 0.0
motor = Motor(forward=23, backward=24, pwm=True)
speed = int(0)

# Controller LED
xbox_on = LED(25)
xbox_on.off()

xbox_dev = '/dev/input/event1'
while xbox_dev not in evdev.list_devices():
    # print('Waiting for Controller')
    xbox_on.on()
    time.sleep(0.5)
    xbox_on.off()
    time.sleep(0.5)
    
xbox_on.on()
dev = InputDevice(xbox_dev)
# attched first

axis = {
    ecodes.ABS_X: 'ls_x',  # 0 - 65,536   the middle is 32768
    ecodes.ABS_Y: 'ls_y',
    ecodes.ABS_Z: 'rs_x',
    ecodes.ABS_RZ: 'rs_y',
    ecodes.ABS_BRAKE: 'lt',  # 0 - 1023
    ecodes.ABS_GAS: 'rt',

    ecodes.ABS_HAT0X: 'dpad_x',  # -1 - 1
    ecodes.ABS_HAT0Y: 'dpad_y'
}

center = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

last = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

for event in dev.read_loop():
    # calibrate zero on Y button
    if event.type == ecodes.EV_KEY:                     # Xbox Label
        if categorize(event).keycode[0] == "BTN_WEST":  # lt button
            center['ls_x'] = last['ls_x']
            center['ls_y'] = last['ls_y']
            center['rs_x'] = last['rs_x']
            center['rs_y'] = last['rs_y']
            # print('calibrated')
        elif categorize(event).keycode[0] == "BTN_Z":  # rt button
            pass
        elif categorize(event).keycode[0] == "BTN_TL":  # left menu
            pass
        elif categorize(event).keycode[0] == "BTN_TR":  # right menu
            pass
        elif categorize(event).keycode[0] == "BTN_A":  # A button
            pass
        elif categorize(event).keycode[0] == "BTN_B":  # B button
            pass
        elif categorize(event).keycode[0] == "BTN_C":  # X button
            pass
        elif categorize(event).keycode[0] == "BTN_X":  # Y button
            pass
        
    # read stick axis movement
    elif event.type == ecodes.EV_ABS:
        if axis[event.code] in ['ls_x', 'ls_y']:
            last[axis[event.code]] = event.value

            value = event.value - center[axis[event.code]]

            if abs(value) <= CENTER_TOLERANCE:
                value = 0

            if axis[event.code] == 'ls_x':
                dc = range * (value/32768) + mid
                if dc < min:
                    dc = min
                if dc > max:
                    dc = max
                # print(value, dc)
                pwm.change_duty_cycle(dc)

        elif axis[event.code] in ['lt', 'rt']:
            if  axis[event.code] == 'lt':
                rev = event.value
                # print('Reverse: ', event.value)
                if  fwd == 0:
                    motor.backward(event.value/1023)
                else:
                    motor.backward(0.0)
            if  axis[event.code] == 'rt':
                fwd = event.value
                # print('Forward: ', event.value)
                if rev == 0:
                    motor.forward(event.value/1023)
                else:
                    motor.forward(0.0)
