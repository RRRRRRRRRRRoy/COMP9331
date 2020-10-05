import socket
import sys
import time

# Change the wait delay if needed
# 600ms 
wait_delay = 0.6
# set the min max and avg value as 0
min_result = max_result = avg_result = 0

if len(sys.argv) <= 1:
    print("Need arguments for Address and Port Number!")
    sys.exit()

#####################################################################################################
# Define the connection
# format : Address + Port Number
# we can get the servername from the second argument of command-line, which is sys.argv[1]
# we can also get the port number from the third argument of command-line, which is sys.argv[2]
#####################################################################################################
server_name = sys.argv[1]
string_port_num = sys.argv[2]
port_number = int(string_port_num)
# Wrap up the address information as a tuple
address_info = (server_name,port_number)


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
seq_number = 3331
count = 0
index = 0

# from 0 to 14 which is 15 numbers
# for index in range(0,15,1):
while index < 15:
    # record the time sending ---> time stamp
    send_time = time.time()
    blank_str = " " 
    str_message = "PING" + blank_str + str(index + seq_number) + blank_str + str(send_time) + "\r\n"
    # encode the message use utf-8, then send the message to the target address
    message_2_UTF8 = str_message.encode("utf-8")
    # address_info which contains the infomation 
    client_socket.sendto(message_2_UTF8,address_info)
    
    # 1st situation --------> send the file successfully
    # if not return time out
    while time.time() <= send_time + wait_delay:
        try:
            modified_message,server_address =[item for item in client_socket.recvfrom(2048)]
        except socket.error as error:
            # continue to receive from socket until get nothing
            continue
        # check the message not null
        if modified_message:
            # check the address not null
            if server_address:
                # doing the decode process
                decode_message = modified_message.decode('utf-8')
                # message without header
                m_rece = decode_message[5:]
                # get the index of blank
                blank_index_mrece = m_rece.index(' ')
                if int(index + seq_number) == int(m_rece[0:blank_index_mrece]):
                    # current time - sending time = rtt_time
                    rtt_time = time.time() * 1000 - send_time*1000
                    result_list.append(rtt_time)
                    print(f"ping to {server_name}, seq = {seq_number + index}, rtt={round(result_list[count])}ms")
                    count = count + 1
                    index = index + 1
                    break
    # 2nd situation --------> time out!
    # check the time stamp and print the value
    else:
        if time.time() > send_time + wait_delay:
            print(f"ping to {server_name}, seq = {seq_number + index}, time out") 
            index += 1

        
# get the min rtt time
min_result = min([item for item in result_list])
# get the max rtt time
max_result = max([item for item in result_list])
# get the avg rtt time
avg_result = sum([item for item in result_list]) / len(result_list)

print(f"min: {round(min_result)}ms, max: {round(max_result)}ms, avg: {round(avg_result)}ms")
client_socket.close()