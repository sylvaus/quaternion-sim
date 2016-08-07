import socket
import sys
import time
import threading
import queue
import numpy as np

class CellPhoneConnector(object):

    def __init__(self, addr, port):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.server_address = (addr, port)
        print(sys.stderr, 'starting up on %s port %s' % self.server_address)
        self.sock.bind(self.server_address)

        self.thread = None
        self.queue = queue.Queue()
        self.values = []


        for i in range(0,1):
            self.values.append(np.array([0,0,0]))

    def start_communication(self):
        # Listen for incoming connections

        self.thread = threading.Thread(target=self.com_thread)
        self.thread.daemon = True
        self.thread.start()


    def com_thread(self):
        self.sock.listen(1)

        while True:
            # Wait for a connection
            print(sys.stderr, 'waiting for a connection')
            connection, client_address = self.sock.accept()
            try:
                print(sys.stderr, 'connection from', client_address)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(500).decode()
                    values = self.parse_data(data)
                    if not(values == None):
                        #filtering
                        self.values[0] = 1/4.0*(3.0*self.values[0] + value[0])
                        self.queue.put(self.values[0])
                        print(value)

            finally:
                # Clean up the connection
                connection.close()

    def parse_data(self, data):
        result = []

        if data is not "":
            measures = data.split("[")
            for measure in measures:
                if "]" in measure:

                    msg = measure.split(";")
                    result.append([msg[0],
                                [msg[i] for i in range(1,len(msg))]])


            print(result)

        return None



def test():
    connector = CellPhoneConnector("192.168.0.23", 5005)
    connector.start_communication()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    test()