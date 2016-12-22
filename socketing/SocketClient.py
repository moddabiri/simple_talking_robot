from SocketNode import SocketNode
import socket
import time

class SocketClient(SocketNode):
    """description of class"""
    def __init__(self, ip, send_port, recv_port, on_message):
        self.ip = ip
        self.send_port = send_port
        self.recv_port = recv_port
        self._com_thread=None

        send_connection = SocketClient._get_connection(ip, send_port)
        recv_connection = SocketClient._get_connection(ip, recv_port)
        super(SocketClient, self).__init__(send_connection, recv_connection, on_message)

    send_port=0
    recv_port=0
    ip=""
    _com_thread=None

    @staticmethod
    def _get_connection(ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        retry_counter = 100
        print("Connecting to host %s:%d"%(ip,port))
        while True:
            try:
                sock.connect((ip, port))
                break
            except Exception as ex:
                print(str(ex))
                if retry_counter > 0 and ('[Errno 111]' in str(ex) or '[Errno 10061]' in str(ex)):
                    print("Host is unavailable, retrying in 5 seconds...")
                    time.sleep(5)
                    retry_counter -= 1
                else:
                    print("Maximum number of retries reached. Could not connect to the server. halting for port %d..."%port)
                    raise

        print("Connection to server is established on port %d."%port)

        return sock

if __name__ == "__main__":
    def on_message(message):
        print("[CLIENT]: Received a message: %s"%message)
    client = SocketClient('127.0.0.1', 9051, 9050, on_message)
    client.start()

    while True:
        client.send_message("Client is saying hi...")
        time.sleep(2)