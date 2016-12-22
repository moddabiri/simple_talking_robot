__author__ = "Mohammad Dabiri"
__copyright__ = "Free to use, copy and modify"
__credits__ = ["Mohammad Dabiri"]
__license__ = "MIT Licence"
__version__ = "0.0.1"
__maintainer__ = "Mohammad Dabiri"
__email__ = "moddabiri@yahoo.com"

import net_helpers as neth
import sys_helpers as sysh
import time

CONST_STATE_UPDATE_FREQUENCY_SEC = 60

state=None

def get_cpu_temperature():
    t = sysh.execute_unix("/opt/vc/bin/vcgencmd measure_temp")
    return float(t.split('=')[1].split('\'')[0]) 

def update_stats(initial_state=None):
    global state

    if initial_state:
        state = initial_state

    try:
        state.cpu_temp = get_cpu_temperature()
        state.internet = neth.internet_on()
        print("Internet is %s, Temp: %f'C"%("ON" if state.internet else "OFF", state.cpu_temp))
    except:
        raise

def start_cycle(shared_state):
    global state
    state = shared_state
    while True:
        update_stats()
        time.sleep(CONST_STATE_UPDATE_FREQUENCY_SEC)