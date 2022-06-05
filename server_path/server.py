import socket
import _thread
import json
from datetime import datetime


class Server():

    messages = []

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

            self.send_last_messages(connection)

            while True:
                data = connection.recv(64).decode('utf-8')
                if data != '':
                    self.multicast_json(data, owner=connection)
                else:
                    return
        except:
            print(f'{self._get_current_time()} {client_name} left the room !!')
            self.users_table.pop(connection)
            connection.close()

    def _get_current_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def multicast_json(self, message, owner=None):
        data = {'name': self.users_table[owner], 'message': message}
        data_json = json.dumps(data)
        self.messages.append(data_json)
        for conn in self.users_table:
            conn.sendall(bytes(data_json, encoding='utf-8'))

    def send_last_messages(self,new_client=None):
        text = '~'.join(self.messages)
        new_client.send(bytes(text, encoding='utf-8'))

    def multicast(self, message, owner=None):
        for conn in self.users_table:
            data = f'{self.users_table[owner]}~{message}'
            conn.sendall(bytes(data, encoding='utf-8'))


if __name__ == "__main__":
    Server()