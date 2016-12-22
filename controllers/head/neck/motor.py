__author__ = "Mohammad Dabiri"
__copyright__ = "Free to use, copy and modify"
__credits__ = ["Mohammad Dabiri"]
__license__ = "MIT Licence"
__version__ = "0.0.1"
__maintainer__ = "Mohammad Dabiri"
__email__ = "moddabiri@yahoo.com"

from servo_control.ABE_ServoPi import PWM
from servo_control.ABE_helpers import ABEHelpers
import os

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
pwm = PWM(bus, 0x40)

servo_pan_min = 250
servo_pan_max = 450

servo_tilt_min = 350
servo_tilt_max = 450

pwm.set_pwm_freq(60)
pwm.output_enable()

tilt_state = servo_tilt_min+int((servo_tilt_max-servo_tilt_min)/2)
pan_state = servo_pan_min+int((servo_pan_max-servo_pan_min)/2)

def move_head(direction, steps):
    global tilt_state
    global pan_state

    if 'up' in direction:
        new_tilt_state = tilt_state + steps
    elif 'down' in direction:
        new_tilt_state = tilt_state - steps
    else:
        new_tilt_state = tilt_state

    if 'right' in direction:
        new_pan_state = pan_state - steps
    elif 'left' in direction:
        new_pan_state = pan_state + steps
    else:
        new_pan_state = pan_state

    my_print("Moving head to (%d,%d) current: (%d,%d) - Direction: %s"%(new_tilt_state, new_pan_state, tilt_state, pan_state, direction))
    move_head_to(new_tilt_state, new_pan_state)

def move_head_to(tilt_target, pan_target):
    global tilt_state
    global pan_state
    global pwm

    tilt_target = max(min(tilt_target,servo_tilt_max), servo_tilt_min)
    pan_target = max(min(pan_target,servo_pan_max), servo_pan_min)

    while(True):
        if tilt_target == tilt_state and pan_target == pan_state:
            break

        if not tilt_state == tilt_target:
            if tilt_target > tilt_state:
                tilt_state +=1
            else:
                tilt_state -=1
                
            pwm.set_pwm(0, 0, tilt_state)

        if not pan_state == pan_target:
            if pan_target > pan_state:
                pan_state +=1
            else:
                pan_state -=1

            pwm.set_pwm(1, 0, pan_state)
        
        time.sleep(0.005)

def move_to_center(immediate=False):
    global pwm
    global servo_tilt_min
    global servo_tilt_max
    global servo_pan_min
    global servo_pan_max

    new_tilt_state = servo_tilt_min+int((servo_tilt_max-servo_tilt_min)/2)
    new_pan_state = servo_pan_min+int((servo_pan_max-servo_pan_min)/2)
    my_print("Moving to %d,%d"%(new_tilt_state, new_pan_state))
    if immediate:
        pwm.set_pwm(0, 0, new_tilt_state)
        pwm.set_pwm(1, 0, new_pan_state)
    else:
        move_head_to(new_tilt_state, new_pan_state)

def move_by_pixel(x, y):
    global tilt_state
    global pan_state

    tilt = int(y/3.8)
    pan = int(x/3.8)
    print("Moving from (%d,%d) to (%d,%d)"%(tilt_state, pan_state, tilt_state-tilt, pan_state+pan))
    move_head_to(tilt_state-tilt, pan_state+pan)

def look_around(onLook):
    global tilt_state
    global pan_state

    while tilt_state < servo_tilt_max:
        move_head('up', 50)
        result = onLook()
        if result:
            return result

    while pan_state < servo_pan_max:
        move_head('left', 50)
        result = onLook()
        if result:
            return result

    while pan_state > servo_pan_min:
        move_head('right', 50)
        result = onLook()
        if result:
            return result

    

    while tilt_state > servo_tilt_min:
        move_head('down', 50)
        result = onLook()
        if result:
            return result

    while pan_state < servo_pan_max:
        move_head('left', 50)
        result = onLook()
        if result:
            return result

    while pan_state > servo_pan_min:
        move_head('right', 50)
        result = onLook()
        if result:
            return result

    return None