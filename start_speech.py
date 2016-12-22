__author__ = "Mohammad Dabiri"
__copyright__ = "Free to use, copy and modify"
__credits__ = ["Mohammad Dabiri"]
__license__ = "MIT Licence"
__version__ = "0.0.1"
__maintainer__ = "Mohammad Dabiri"
__email__ = "moddabiri@yahoo.com"

import controllers.head.speech_control as sc
import util.stats as stats
import util.sys_helpers as sysh
import socket
import time
import multiprocessing as mp
import threading as mt
from controllers.State import State
from socketing.SocketClient import SocketClient

state = State()
is_active = True
state_preview_cnt=0

def on_message_from_head(state_json):
    global state_preview_cnt
    global state
    
    head_state = State()
    head_state.from_JSON(state_json)

    state.buddy_ip = head_state.ip

    if state.human_name != head_state.human_name:
        print("Human name changed. Now is %s"%head_state.human_name)

    state.human_name=head_state.human_name
    state_preview_cnt += 1

    if state_preview_cnt > 1000:
        state_preview_cnt=0
        print("Head board: Temp: %f'C, Internet: %s"%(head_state.cpu_temp, head_state.internet))

def start():
    global is_active
    global state

    stats.update_stats(state)
    conv_thread = mt.Thread(target=stats.start_cycle, args=(state,))
    conv_thread.setDaemon(True)
    conv_thread.start()

    state.ip=sysh.get_ip('wlan0')

    connection = connect_to_head()

    def send_shutdown_signal():
        global is_active
        is_active = False
        connection.send_message('SHUTDOWN')

    #initatie the head and camera controls
    conv_thread = mt.Thread(target=sc.start, args=(state, send_shutdown_signal,))
    conv_thread.setDaemon(True)
    conv_thread.start()
    
    while is_active:
        connection.send_message(state.to_JSON())
        time.sleep(0.2)

    conv_thread.join()

def connect_to_head():
    ip = '192.168.1.10'
    send_port = 9051
    recv_port = 9050

    client = SocketClient(ip, send_port, recv_port, on_message_from_head)
    client.start()

    return client

if __name__ == '__main__':
    start()
