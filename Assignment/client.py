# The current package we may use in this assignment
# This part is for client.py file
import socket
import sys
import time
import random
import threading
import datetime
#############################################################################################
################    Check the python version in the terminal    #############################
#############################################################################################
# This part is similar with starting server
if sys.version_info[0] >= 3:
    # The python version is 3 or not
    print("Welcome to use the Client!")
elif sys.version_info[0] < 3:
    # The current python version is not 3
    # This time the Server should show the exception(The wrong message)
    wrong_msg = "The current Client file is written by Python3. Plz change the command and Try again!"
    raise Exception(wrong_msg)

ServerName = [sys.argv[i] for i in range(1,2)]
Serverport = int([sys.argv[i] for i in range(2,3)])
Address_infor = (ServerName, Serverport)
# Can also change to 127.0.0.1
Client_server = 'localhost'

# Create the client
# Source: https://stackoverflow.com/questions/48406991/basic-python-tcp-socket-server-client
Clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Clientsocket.connect(Address_infor)