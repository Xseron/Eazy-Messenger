import socket
import _thread
import threading
from datetime import datetime


class Server():

    def __init__(self):
        # For remembering users
        self.users_table = {}

        # Create a TCP/IP socket and bind it the Socket to the port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 8080)
        self.socket.bind(self.server_address)
        self.socket.setblocking(1)
        self.socket.listen(10)
        print('Starting up on {} port {}'.format(*self.server_address))
        self._wait_for_new_connections()

    def _wait_for_new_connections(self):
        while True:
            connection, _ = self.socket.accept()
            _thread.start_new_thread(self._on_new_client, (connection,))

    def _on_new_client(self, connection):
        try:
            # Declare the client's name
            client_name = connection.recv(64).decode('utf-8')
            self.users_table[connection] = client_name
            print(f'{self._get_current_time()} {client_name} joined the room !!')

            while True:
                data = connection.recv(64).decode('utf-8')
                if data != '':
                    self.multicast(data, owner=connection)
                else:
                    return
        except:
            print(f'{self._get_current_time()} {client_name} left the room !!')
            self.users_table.pop(connection)
            connection.close()

    def _get_current_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def multicast(self, message, owner=None, adres_to=None):
        for conn in self.users_table:
            data = f'{self.users_table[owner]}~{message}'
            print(data)
            conn.sendall(bytes(data, encoding='utf-8'))


if __name__ == "__main__":
    Server()