from SocketNode import SocketNode
import socket
import time

class SocketServer(SocketNode):
    """description of class"""
    def __init__(self, ip, send_port, recv_port, on_message):
        self.ip = ip
        self.send_port = send_port
        self.recv_port = recv_port

        recv_connection = SocketServer._get_connection(ip, recv_port, 1)
        send_connection = SocketServer._get_connection(ip, send_port, 1)
        super(SocketServer, self).__init__(send_connection, recv_connection, on_message)
        self.start()

    send_port=0
    recv_port=0
    ip=""
    _com_thread=None
    
    @staticmethod
    def _get_connection(ip, port, no_of_connections=1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.bind((ip, port))
        sock.listen(no_of_connections)

        print("Established a host connection on %s:%d"%(ip, port))
        connection, client_address = sock.accept()
        print("Connecttion to client on the port %d was established..."%port)

        return connection

if __name__ == "__main__":
    def on_message(message):
        print("[SERVER]: Received a message: %s"%message)
    server = SocketServer('127.0.0.1', 9050, 9051, on_message)
    server.start()

    while True:
        server.send_message("Server is saying hi...")
        time.sleep(2)