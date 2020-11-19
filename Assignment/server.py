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

# This set may used to check whether a second person want to login in the current username
current_client = set()

# record the current threads and threadtile
threads_content = dict()

# This may used to save the current thread for LST command
LST_server = list()

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
            U_pass = line[line.index(" ") + 1:]
            # create them into a dictionary
            client_dict[U_name] = U_pass
