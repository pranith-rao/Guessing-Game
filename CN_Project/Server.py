import socket
import sys
import random
clientNumber = 0
clients = []
statements = {}
order = [None]


def send(c, msg):  # message entered by the client is sent to server
    packet = bytes(str(msg), 'utf-8')  # messages are converted to bytes
    c.send(packet)  # messages in the form of bytes are sent to server


def guess(num):
    for k, v in statements.items():  # reading values from dictionary
        if order[num] == v:
            if k == 'True':
                broadcast("Correct Answer")
                break
            else:
                broadcast("Incorrect Answer")
                break


def broadcast(msg):  # send message to all the connected clients
    for c in clients:
        try:
            send(c, msg)
        except:
            # removes the client from the client array if connection is failed and message is not sent
            clients.remove(c)


def genrateStatements():
    val = random.sample(list(statements.values()), len(statements))
    order.append(val[0])
    order.append(val[1])
    msg = '1. '+order[1]+'\n2. '+order[2]
    return msg


hostname = socket.gethostname()  # will fetch the system host name
ip = socket.gethostbyname(hostname)  # will fetch the system's IP address
port = 9999
# AF_INET represents internet address family and SOCK_STREAM represents protocol that is used to transport messages
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Server running on Host ' + ip + '| Port ' + str(port))

# Bind and Listen
try:
    s.bind((ip, port))  # establishes connection btw the IP and port specified
except socket.error as e:
    print(str(e))
s.listen(6)  # Listen to n client here 6

while True:
    c, addr = s.accept()  # accepts client's IP and socket address
    clientNumber += 1
    clients.append(c)  # appends clients to the client list
    print("Connection " + str(clientNumber) +
          " established from: " + str(addr))
    if clientNumber == 1:
        send(c, 'Guess')

        rcvd = c.recv(1024)  # used to receive message from the client
        # used to decode the message received from client
        truth = bytes(rcvd).decode('utf-8')
        statements['True'] = truth
        print(truth)
        rcvd1 = c.recv(1024)
        false = bytes(rcvd1).decode('utf-8')
        statements['False'] = false
        print(false)

    else:
        send(c, 'Guess the Truth')
        msg = genrateStatements()
        send(c, msg)
        rcvd1 = c.recv(1024)
        ans = bytes(rcvd1).decode('utf-8')
        guess(int(ans))
