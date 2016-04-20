#!/usr/bin python

import socket
import json
import threading
import sys

PORT = 49999

class Client(threading.Thread):
    def __init__(self, (client_conn, client_addr)):
        threading.Thread.__init__(self)
        self.client_conn = client_conn
        self.client_addr = client_addr
        self.size = 2048

    def run(self):
        while True:
            data = None
            try:
                data = self.client_conn.recv(self.size)
            except socket.error, e:
                print(e.message)

            if data is not None:
                try:
                    data = json.loads(data)
                    print("Received : " + str(data))
                    if 'mydata' in data:
                        print(data['mydata'])
                except ValueError:
                    continue

            self.client_conn.close()
            break

class Receiver:
    def __init__(self):
        self.host = self.get_ip_address()
        self.port = 49999
        self.threads = list()
        self.tcp_sock = None

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


    def create_socket(self):
        try:
            self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_sock.bind((self.host, self.port))
            self.tcp_sock.listen(2)
        except socket.error:
            if self.tcp_sock:
                self.tcp_sock.close()
            print("Failure to open socket")
            sys.exit(1)

    def run(self):
        self.create_socket()
        while True:
            client = Client(self.tcp_sock.accept())
            client.start()
            self.threads.append(client)

def main():
    receiver = Receiver()
    receiver.run()

if __name__ == '__main__':
    main()

