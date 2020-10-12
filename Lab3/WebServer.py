import base64
import socket
import time, sys

if sys.version_info[0] < 3:
    raise Exception("Please use Python3 file as the input!")

server_port = int(sys.argv[1])

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.listen(1)

print("Server is ready!")

while True:
    connection_socket = server_socket.accept()[0]
    address = server_socket.accept()[1]
    sentence = connection_socket.recv(2048).decode()
    if sentence:
        URL = sentence[sentence.index("/") + 1 : sentence.index(" HTTP")]
        try:
            get_file = open(URL,'rb')
        except FileNotFoundError:
            