import base64
import socket
import time
import sys

if sys.version_info[0] < 3:
    raise Exception("Please use Python3 file as the input!")

server_port = int(sys.argv[1])
IP_info = ('localhost',server_port)

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind(IP_info)

server_socket.listen(1)

print("Server is ready!")

header_type = {200 : "HTTP/1.1 200 OK\r\nAcept-Ranges: bytes\r\nKeep-Alive: timeout=10, max=100\r\nConnection: " \
                    "Keep-Alive\r\nContent-Type: " \
                    "text/html\r\n\r\n",\
                    404 : "HTTP/1.1 404 Not Found\r\nAcept-Ranges: bytes\r\nKeep-Alive: timeout=10, max=100\r\nConnection: " \
                    "Keep-Alive\r\nContent-Type: " \
                    "text/html\r\n\r\n",\
                    "Not_Found_page":'<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1> <p>The requested ' \
			        'URL was not found on this server.</p></body></html>'}


while True:
    connection_socket,address = [item for item in server_socket.accept()]
    sentence = connection_socket.recv(1024).decode()
    if sentence:
        start_index = sentence.index("/")
        end_index = sentence.index(" HTTP")
        URL = sentence[start_index + 1 : end_index]
