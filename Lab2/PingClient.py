import socket
import sys,time

# Change the wait delay if needed
wait_delay = 1

if len(sys.argv) ==1:
    print("Need arguments for Address and Port No!")
    sys.exit()

#####################################################################################################
# Define the connection
# format : Address + Port Number
# we can get the servername from the second argument of command-line, which is sys.argv[1]
# we can also get the port number from the third argument of command-line, which is sys.argv[2]
#####################################################################################################
server_name = sys.argv[1]
port_num_str = sys.argv[2]
port_number = int(port_number)
Address = (server_name,port_number)


#####################################################################################################
# After, finishing the definition of variables we need to create the socket of client
# We can use the UDP sample provided by the professor
# Source: https://webcms3.cse.unsw.edu.au/static/uploads/course/COMP3331/19T2/9ab191bb260f773e60bc278131e7a54af9576260181b3cfe91911deb3202a93d/UDPClient.py
# Here are some parameters 
# socket.AF_INET is used to set up the connection between the internet and server
# socket.SOCK_DGRAM is for UDP protocal
# We can also find these parameters in docs(include function settimeout())
# Source: https://docs.python.org/3/library/socket.html
#####################################################################################################
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# settimeout is to check the working modes, which are blocking mode and non-blocking mode.
client_socket.settimeout(0)

result_list = list()
count = -1
for index in range(0,10):
    # record the time sending ---> time stamp
    send_time = time.time()
    blank_str = " " 
    str_message = "PING" + blank_str + str(index) + blank_str + str(send_time) + "\r\n"
    message_2_UTF8 = str_message.encode("utf-8")
    client_socket.sendto(message_2_UTF8,Address)
    time_2_receive = time.time() + wait_delay
    while time.time() <= time_2_receive:
        try:
            modified_message,server_address = client_socket.recvfrom(2048)
