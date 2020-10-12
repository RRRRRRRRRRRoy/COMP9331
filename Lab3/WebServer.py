import base64
import socket
import time, sys

if sys.version_info[0] < 3:
    raise Exception("Please use Python3 file as the input!")

server_port = int(sys.argv[1])

server_socket = socket(AF_INET,SOCK_STREAM)