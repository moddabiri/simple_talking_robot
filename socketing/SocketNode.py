__author__ = "Mohammad Dabiri"
__copyright__ = "Free to use, copy and modify"
__credits__ = ["Mohammad Dabiri"]
__license__ = "MIT Licence"
__version__ = "0.0.1"
__maintainer__ = "Mohammad Dabiri"
__email__ = "moddabiri@yahoo.com"

from Queue import Queue
import threading as mt
import time

class SocketNode(object):
    def __init__(self, send_connection, recv_connection, on_message):
        self.send_connection = send_connection
        self.recv_connection = recv_connection
        self.on_message=on_message
        self._data_buffer = ""

    START_IND = "[START]"
    END_IND = "[END]"

    send_connection=None
    recv_connection=None
    message_queue = Queue()
    on_message=None
    _data_buffer = ""
    _keep_running=True
    _queue_lock=mt.Lock()

    def send_message(self, message):
        try:
            self._queue_lock.acquire()
            self.message_queue.put(message)
        finally:
            self._queue_lock.release()

    def _start_listening(self):
        print("Started listening")
        while self._keep_running:
            self.on_message(self._receive_data())
            time.sleep(0.1)

    def _start_sending(self):
        print("Started sending")
        while self._keep_running:
            try:
                self._queue_lock.acquire()
                if not self.message_queue.empty():
                    data = self.message_queue.get()
                    self._send_data(data)
            finally:
                self._queue_lock.release()

            time.sleep(0.1)

    def start(self):
        self._keep_running=True
        mt.Thread(target=self._start_listening).start()
        mt.Thread(target=self._start_sending).start()

    def stop(self):
        self._keep_running=False

    def _receive_data(self):
        while True:
            data = self.recv_connection.recv(1024)
            
            if data:
                self._data_buffer = self._data_buffer + data

                if SocketNode.END_IND in self._data_buffer:
                    new_message = self._data_buffer.split(SocketNode.END_IND)[0].replace(SocketNode.START_IND, '')                    
                    self._data_buffer = self._data_buffer[self._data_buffer.index(SocketNode.END_IND)+5:]
                    return new_message    
            else:
                return None              

    def _send_data(self, message):
        self.send_connection.send('%s%s%s'%(SocketNode.START_IND, message, SocketNode.END_IND))

    def __exit__(self, exc_type, exc_value, traceback):
        if self.send_connection:
            self.send_connection.close()

        if self.recv_connection:
            self.recv_connection.close()
        
        