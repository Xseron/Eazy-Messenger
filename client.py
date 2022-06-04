import sys
import socket
import threading


class Client():

    ms = None

    def __init__(self,client_name,ms):
        self.ms = ms
        self.client_name = client_name

    def start(self):
        print("Connect to server")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 8080)
        self.socket.connect(self.server_address)
        self.socket.setblocking(1)
        self.socket.send(bytes(self.client_name, encoding='utf-8'))
        receive = threading.Thread(target=self._client_receive)
        receive.start()

    def client_send(self,text):
        sys.stdout.write("\x1b[1A\x1b[2K") # Delete previous line
        self.socket.send(bytes(text, encoding='utf-8'))

    def _client_receive(self):
        while True:
            try:
                text = self.socket.recv(1024).decode("utf-8").split('~')
                self.ms.send_message(text[0],text[1])
                print(self.socket.recv(1024).decode("utf-8"))
            except:
                self.socket.close()
                return