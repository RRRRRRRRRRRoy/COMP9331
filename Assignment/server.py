# The current package we may use in this assignment
# This part is for server.py file
import socket
import sys
import time
import threading
import datetime as dt
#############################################################################################
################    Check the python version in the terminal    #############################
#############################################################################################
if sys.version_info[0] >= 3:
    # The python version is 3 or not
    print("Welcome to use the Server!")
elif sys.version_info[0] < 3:
    # The current python version is not 3
    # This time the Server should show the exception(The wrong message)
    wrong_msg = "The current Server file is written by Python3. Plz change the command and Try again!"
    raise Exception(wrong_msg)

#############################################################################################
################   Get the User Data from Credentials.txt file  #############################
#############################################################################################
# When we Login in the server we should get the Username and PWD from the file
# This process can be change by connecting to the Database and get data from it
client_dictionary = dict()

# Shutdown_flag default is False -----> Server is not shutdown
SHUTDOWN = False

# This set may used to check whether a second person want to login in the current username
# Set cannot exist 2 same elements
current_client = set()

# record the current threads and threadtile
threads_dictionary = dict()

# This may used to save the current thread for LST command
LST_server = list()

# encode Type
encode_type = 'utf-8' 

# Keywords_dict
global Keywords_dict = {"to":"time_out",'sd':"shutting_down",'iu':"inuse","crt":'correct'}

# wraping these function to check timeout and shutdown
def check_timout_N_Shutdown(keyword):
    keyword = Keywords_dict[keyword].upper()
    encode_msg = keyword.encode(encode_type)
    connect_socket.send(encode_msg)
    connect_socket.close()
    close = True

def Check_same(kind,string_Data):
    space_index = string_Data.index(" ")
    username = string_Data[0:space_index]
    if kind == "username":
        if username == "LOGIN_USERNAME".upper():
            return True
        else:
            return False
    elif kind == "password":
        if username == "LOGIN_PASSWORD".upper():
            return True
        else:
            return False


# Usingt with open can omit the step of Writing Close
# Here is the reason of using with
# Source: https://stackoverflow.com/questions/21275836/if-youre-opening-a-file-using-the-with-statement-do-you-still-need-to-close
with open("credentials.txt") as file:
    for index in range(len(file.readlines())):
        if file.readlines[index]:
            line = file.readlines[index].strip('\n')
            # The format is : Username  Password
            # Slice the String and get username pwd
            U_name = line[:line.index(" ")]
            U_password = line[line.index(" ") + 1:]
            # create them into a dictionary
            client_dict[U_name] = U_password

def client_connection(connection_socket, address):
    # change the previous the container to the global variable
    global client_dictionary
    global current_client
    global SHUTDOWN
    global threads_dictionary

    # This flag is used to check when the current connection is closed or not
    close_flag = False
    # Set the current timeout for Server
    connection_socket.settimeout(2)

    # Counter: count the time of recving data
    global recv_counter = 90 

    # In this kind of system, we should implement it in a Endless loop!
    while 1:
        # Check whether the server is start or shutdown
        # if the server is shutdown, the SHUTDOWN will become True, Then into the if layer
        if SHUTDOWN:
            # If shutdown sending the client shuttding down key words to shutdown
            # After seding the message close the connection
            # And Set the close flag to True
            check_timout_N_Shutdown('sd')
            break
        # From 0 to 90 count the time 
        # In this period getting the data from the client and doing the decode process
        for timer in range(0,recv_counter):
            # Avoiding exception
            try:
                string_Data_encode = connect_socket.recv(1024)
                string_Data = string_Data_encode.decode(encode_type)
                # check the data is empty or not 
                # empty ---> continue receive
                if not string_Data:
                    continue
                else:
                    # Getting the data already ----> break
                    break
            except socket.timeout:
                # Check the shutdown of the server
                if not SHUTDOWN:
                    continue
                else:
                    break
            # After outof the range counter which is from 0-90
            # then print time out and sending the key words to the client
            else:
                print("Time out!")
                # check timeout
                check_timout_N_Shutdown('to')
                break
            # Avoding sending message after shutting down
            if SHUTDOWN:
                # check shutdown
                check_timout_N_Shutdown('sd')
                break
            
            # Getting the username
            # check string data string_Data
            if Check_same('username',string_Data):
            # if strData[:strData.index(" ")] == "LOGIN_USERNAME":
                print("login_username")
                space_index = string_Data.index(" ") 
                string_Data = string_Data[space_index + 1:]
                Username = string_Data
                print("username:", Username)
                if Username in current_client:
                    msg_keyword = Keywords_dict["iu"]
                    msg_keyword = msg_keyword.upper()
                    msg_keyword = msg_keyword.encode()
                    connect_socket.send(msg_keyword)
                    continue
                
