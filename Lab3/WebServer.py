
import base64
import socket
import time
import sys

################################################################################################
# Get the current python version
# Avoiding the version error auto-test in the school server
# Using the sys.version_info[0] to check the current version
# Source: https://stackoverflow.com/questions/52359805/is-sys-version-info-reliable-for-python-version-checking
################################################################################################
if sys.version_info[0] >= 3:
    # print(f"The current version of Python is Python{sys.version_info[0]}")
    print("Welcome to use WebServer!")
elif sys.version_info[0] < 3:
    wrong_msg = "The current WebServer is written in Python3. Pls change the command"
    raise Exception(wrong_msg)

# get the IP address and server port
# wrap them into a tuple
IP_info = ('localhost',int(sys.argv[1]))

################################################################################################
# The same way like writing the PingClient
# Different : PingClient is UDP , WebServer is TCP which needs to bind and set up the connection
################################################################################################
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(IP_info)
server_socket.listen(1)
# show the result in the terminal -----> Server is ready
print("Server is ready to receive request!")

# Using the dictionary is easier than using String
header_type = {200 : "HTTP/1.1 200 OK\r\nAcept-Ranges: bytes\r\nKeep-Alive: timeout=10, max=100\r\nConnection: " \
                    "Keep-Alive\r\nContent-Type: " \
                    "text/html\r\n\r\n",\
                    404 : "HTTP/1.1 404 Not Found\r\nAcept-Ranges: bytes\r\nKeep-Alive: timeout=10, max=100\r\nConnection: " \
                    "Keep-Alive\r\nContent-Type: " \
                    "text/html\r\n\r\n",\
                    "Not_Found_page":'<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1> <p>The requested ' \
			        'URL was not found on this server.</p></body></html>'}

# Using this function to chenge string to utf-8 bytes
def change_bytes(key,header_type):
    bytes_value = bytes(header_type[key],'utf-8')
    return bytes_value

################################################################################################
# From the http header
# The file name is behind '/' before " HTTP"
# getting the index of these characters and using the slice method to cut it
# Source: https://stackoverflow.com/questions/8035900/how-to-get-filename-from-content-disposition-in-headers
################################################################################################
while True:
    connection_socket,address = [item for item in server_socket.accept()]
    sentence = connection_socket.recv(2048).decode()
    if sentence:
        start_index = sentence.index("/")
        end_index = sentence.index(" HTTP")
        file_name = sentence[start_index + 1 : end_index]       
################################################################################################
# Check whether the file is in the directory
# Using the try-catch function
# exist -----> OK -----> send name to server and show the resource
# Not exist -----> NOT Found -----> show the NOT FOUND page(in the previous dictionary)
# You can also find this function in Stack Overflow
# Source: https://stackoverflow.com/questions/22366282/python-filenotfound
################################################################################################
        try:
            get_file = open(file_name,'rb')
        except FileNotFoundError:
            connection_socket.send(change_bytes(404,header_type))
            connection_socket.send(change_bytes("Not_Found_page",header_type))
            print("Fail to get the request! T_T")
            # not found then close socket
            connection_socket.close()
            continue

################################################################################################
# Question Source: https://webcms3.cse.unsw.edu.au/COMP3331/20T3/resources/51954
# Only one kind of test HTML file which is index.html
# just check whether the name of file is same or not
################################################################################################
        connection_socket.send(change_bytes(200,header_type))
        if file_name == "index.html":
            file_content = get_file.read()
            connection_socket.send(file_content)
            print("Getting the request successfully! ^_^")
################################################################################################
# Second situation ------> showing picture
# Use base64 to encode picture and show on the website
# Step 1 : Read file with buffer reader
# Step 2 : using base64.b64encode to encode the picture
# Step 3 : Send the encode pic to the browser
# Source: https://stackoverflow.com/questions/3715493/encoding-an-image-file-with-base64
################################################################################################
        else:
            picture_content = get_file.read()
            pic_encode = base64.b64encode(picture_content)
            # Picture with HTML tag ----> Show the picture
            connection_socket.send(b'<img src="data:image/jpg;base64,' + pic_encode + b'">')
            print("Getting the request successfully")
    # After getting the request, showing the content and clost socket
    connection_socket.close()
