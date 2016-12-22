import util.stats as stats
import controllers.head.head_control as hc
import util.sys_helpers as sysh
import socket
import time
import multiprocessing as mp
import threading as mt
from controllers.State import State
from socketing.SocketServer import SocketServer

state = State()
state_preview_cnt=0

def on_message_from_speech(state_json):
    global state_preview_cnt
    global state
    
    if state_json == "SHUTDOWN":
        sysh.shutdown()
        return

    speech_state = State()
    speech_state.from_JSON(state_json)

    state.buddy_ip=speech_state.ip
    state_preview_cnt += 1

    if state_preview_cnt > 1000:
        state_preview_cnt=0
        print("Speech board: Temp: %f'C, Internet: %s"%(speech_state.cpu_temp, speech_state.internet))

def start():
    global state

    stats.update_stats(state)
    stat_thread = mt.Thread(target=stats.start_cycle, args=(state,))
    stat_thread.setDaemon(True)
    stat_thread.start()

    state.ip=sysh.get_ip('wlan0')

    connection = connect_to_speech()

    #initatie the head and camera controls
    head_thread = mt.Thread(target=hc.start, args=(state,))
    head_thread.setDaemon(True)
    head_thread.start()
    
    while True:
        connection.send_message(state.to_JSON())
        time.sleep(0.2)

    head_thread.join()

def connect_to_speech():
    eth_ip = sysh.get_eth0_ip()
    send_port = 9050
    recv_port = 9051

    server = SocketServer(eth_ip, send_port, recv_port, on_message_from_speech)
    server.start()

    return server

if __name__ == '__main__':
    start()