import socket
import sys


hostname = socket.gethostname()  # will fetch the system host name
ip = socket.gethostbyname(hostname)  # will fetch the system's IP address
port = 9999
s = socket.socket()  # creating socket object
print('Client running on Host ' + ip + '| Port ' + str(port))
s.connect((ip, port))  # establishes connection between IP address and port


def send(c, msg):  # message entered by the client is sent to server
    packet = bytes(str(msg), 'utf-8')
    c.send(packet)  # messages in the form of bytes are sent to server


msg = s.recv(1024).decode('utf-8')  # message received from server is decoded

if msg == 'Guess':
    print('Enter a True statement')
    msg1 = input()
    send(s, msg1)  # sends the true statement to server to broadcast
    print('Enter a False statement')
    msg2 = input()
    send(s, msg2)  # sends the false statement to server to broadcast
    # message received from server is decoded
    msg = s.recv(1024).decode('utf-8')
    print(msg+" guessed by Player 2")
else:
    print(' Guess the TRUE Statement\n Wait for Player 1 to enter the details...\n Enter which is true 1 or 2')
    msg = s.recv(1024).decode('utf-8')
    print(msg)
    ans = input()  # takes input from player 2
    if ans == '1' or ans == '2':
        send(s, ans)
        msg1 = s.recv(1024)
        data = bytes(msg1).decode('utf-8')
        print(data)
    else:
        print('Wrong')


# terminate the connection btw the client and server
s.shutdown(socket.SHUT_RDWR)
s.close()
