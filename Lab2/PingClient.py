import socket
import sys
import time

# Change the wait delay if needed
# 600ms 
wait_delay = 0.6

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
port_number = int(sys.argv[2])


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

for index in range(15):
    # record the time sending ---> time stamp
    send_time = time.time()
    blank_str = " " 
    str_message = "PING" + blank_str + str(index + seq_number) + blank_str + str(send_time) + "\r\n"
    client_socket.sendto(str_message.encode("utf-8"),(server_name,port_number))
    time_2_receive = time.time() + wait_delay
    # wait_dely to receive
    while time.time() <= time_2_receive:
        try:
            modified_message,server_address = client_socket.recvfrom(2048)
        except socket.error as error:
            # continue to receive from socket until get nothing
            continue
        if modified_message is True and server_address is True:
            m_rece = modified_message.decode('utf-8')[5:]
            if (index + seq_number) == int(m_rece[:m_rece.index(' ')]):
                result_list.append((time.time()-send_time)*1000)
                print(f"ping to {server_name}, seq = {seq_number + index}, rtt={round(result_list[count])}ms")
                count += 1
                break
    else:
        print(f"ping to {server_name}, seq = {seq_number + index}, time out")
print(f"min: {round(min(result_list))}ms, max: {round(max(result_list))}ms, avg: {round(sum(result_list)/len(result_list))}ms")
client_socket.close()