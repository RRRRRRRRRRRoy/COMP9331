import base64
import socket
import time, sys

if sys.version_info[0] < 3:
    raise Exception("Please use Python3 file as the input!")

server_port = int(sys.argv[1])

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind(('127.0.0.1',server_port))

server_socket.listen(1)

connection_socket = server_socket.accept()[0]

address = server_socket.accept()[1]

sentence = connection_socket.recv(1024).decode()

print(sentence)