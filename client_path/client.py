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

    def end(self):
        self.socket.close()

    def client_send(self,text):
        sys.stdout.write("\x1b[1A\x1b[2K") # Delete previous line
        self.socket.send(bytes(text, encoding='utf-8'))

    def _client_receive(self):
        try:
            while True:
                text = self.socket.recv(1024).decode("utf-8")
                if(text!=''):
                    self.ms.send_message(text)
                    print(text)
                else:
                    print('err')
        except:
            print("Exit_program")