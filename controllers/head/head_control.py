import time
from controllers.state.state_machine import StateMachineNode
import numpy as np
from datetime import datetime
from State import State

mock = False
verbose=False
env_state = None

def my_print(message):
    if verbose:
        print(message)

if mock:
    class PWM_Mock():
        def set_pwm_freq(self, f):
            pass
        def output_enable(self):
            pass
        def set_pwm(self, index, a, state):
            my_print("PWM %d set to %d"%(index, state))

    pwm = PWM_Mock()

    class Camera_Mock():
        def capture(self, filename):
            my_print("Camera is capturing")
            

    camera = Camera_Mock()

    class Recognizer_Mock():
        def train():
            my_print("Recognizer: Training")

        def save(path):
            my_print("Recognizer: Saving to path")

    class Cascade_Mock():
        def detectMultiScale(image):
            my_print("Detecting")

    faceCascade = Cascade_Mock()
    recognizer = Recognizer_Mock()
else:
    import neck.motor as neck_motor
    import sight.camera as camera
    import os
   
states = {'R-INIT':         0,
          'R-IDLE':         1,
          'R-LOOKAROUND':   2,
          'R-FOLLOW':       3
          }

activations = {
    'INIT-DONE':                      0,
    'LOST-TARGET':           1,
    'FOUND-TARGET':          2,
    'LOOK-AROUND':           3,
    'IDLE':                  4
}

def move_and_go(tilt_target, pan_target, activation):
    neck_motor.move_head_to(tilt_target, pan_target)
    return activation

def wait(seconds):
    time.sleep(seconds)
    return "NULL"

idle_counter=0

def idle():
    global idle_counter
    neck_motor.move_to_center()
    idle_counter += 1

    if idle_counter > 10:
        idle_counter = 0
        return "LOOK-AROUND"

    return wait(1)

def capture():
    global env_state

    camera.capture()
    faces = camera.detect()
    recognized = camera.recognize(faces)
        
    if len(recognized) > 0:
        return 'FOUND-TARGET' ,recognized[0],  (x, y, w, h, predict_image.shape[0], predict_image.shape[1])

    return None, None, None

def observe():
    #Capture
    #Look for the familar face
    #if found return "TARGET-FOUND"
    #elif: if all around is observed return "IDLE"

    global env_state

    env_state.human_name = "human"

    def onLook():
        result, target, location = capture()
        if result:
            return result
        return None

    result = neck_motor.look_around(onLook)
    if result:
        return result

    return 'IDLE'

lost_counter = 0

def follow():
    global servo_pan_min
    global servo_pan_max
    global servo_tilt_min
    global servo_tilt_max
    global lost_counter

    print("Following...")

    result, target, location = capture(True)
    if not result:
        print('LOST-TARGET' if lost_counter > 3 else 'NULL')
        consider_lost = lost_counter > 3
        lost_counter = 0 if consider_lost else lost_counter + 1
        return 'LOST-TARGET' if consider_lost else 'NULL'
    else:
        env_state.human_name = target

    lost_counter = 0
    image_center = (location[5]/2, location[4]/2)
    face_center = (location[0]+location[2]/2, location[1]+location[3]/2)
    movement_pixels = (face_center[0]-image_center[0],face_center[1]-image_center[1])
    print("Moveing (%d,%d) pixels"%(movement_pixels[0], movement_pixels[1]))
    neck_motor.move_by_pixel(movement_pixels[0], movement_pixels[1])

    #time.sleep(0.1)
    return 'NULL'

def start(state):
    global tilt_state
    global camera_temp_capture

    env_state = state
    neck_motor.move_to_center(True)

    state_init = StateMachineNode('R-INIT', lambda silent, accepted:move_and_go(neck_motor.tilt_state, neck_motor.pan_state, 'INIT-DONE'))
    
    state_idle = StateMachineNode('R-IDLE', lambda silent, accepted:idle())
    state_init.add_edge(state_idle, 'INIT-DONE')
    state_idle.add_edge(state_idle, 'NULL')

    state_look = StateMachineNode('R-LOOK-AROUND', lambda silent, accepted:observe())
    state_idle.add_edge(state_look, 'LOOK-AROUND')
    state_look.add_edge(state_look, 'NULL')
    state_look.add_edge(state_idle, 'IDLE')

    state_follow = StateMachineNode('R-FOLLOW', lambda silent, accepted:follow())
    state_look.add_edge(state_follow, 'FOUND-TARGET')
    state_follow.add_edge(state_follow, 'NULL')
    state_follow.add_edge(state_look, 'LOST-TARGET')

    StateMachineNode.start(state_init)

if __name__ == "__main__":
    verbose=True
    start(State())