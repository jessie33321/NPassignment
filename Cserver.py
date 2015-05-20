# Tcp Chat server

import socket, select, time

#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__":

    # pre-built account & password
    account = ["john", "mary","makuci"]
    password = ["111","222","333"]
    state = ["\0","\0","\0"]

    # List to keep track of socket descriptors
    offline_msg = []
    offline_rcv = []
    CONNECTION_LIST = []
    CNCT_NAME = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2

    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print "Chat server started on port " + str(PORT)

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                sockfd.send("login as:")
                acc = sockfd.recv(RECV_BUFFER)
                acc = acc.rstrip('\n')

                # check acount
                if acc in account:
                    sockfd.send("password:")
                    pas = sockfd.recv(RECV_BUFFER)
                    pas = pas.rstrip('\n')

                    if pas == password[account.index(acc)]:
                        sockfd.send("login successful\n")
                        CONNECTION_LIST.append(sockfd)
                        CNCT_NAME.append(acc)
                        print "Client %s connected" % acc

                        #send off-line message
                        while acc in offline_rcv:
                            time.sleep(0.05)
                            sockfd.send(offline_msg[offline_rcv.index(acc)])
                            offline_msg.pop(offline_rcv.index(acc))
                            offline_rcv.remove(acc)

                    else:
                        sockfd.send("password is wrong!\n")

                else:
                    sockfd.send("This account doesn't exist!\n")

            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    data = sock.recv(RECV_BUFFER)
                    sender = CNCT_NAME[CONNECTION_LIST.index(sock) - 1]
                    if data == "listuser\n":
                        msg='\0'
                        for name in CNCT_NAME:
                            msg = msg + name + '\t' + state[account.index(name)] + '\n'
                        sock.send(msg)

                    elif data == "change state\n":
                        sock.send("new state:")
                        msg = sock.recv(RECV_BUFFER)
                        state[CONNECTION_LIST.index(sock) - 1] = msg.rstrip('\n')
                        sock.send('\0')

                    elif data[0:4] == "send":
                        #need to modify
                        send = data.split()
                        if send[1] in CNCT_NAME:
                            s = CONNECTION_LIST[CNCT_NAME.index(send[1]) + 1]
                            msg = send[2] + ' (from ' + sender + ')' + '\n'
                            s.send(msg)
                            sock.send('\0')
                        elif send[1] in account:
                            offline_rcv.append(send[1])
                            offline_msg.append('Message from ' + sender + ": " + send[2] + '\n')
                            sock.send('\0')
                        else:
                            sock.send("This user doesn't exist\n")

                    elif data[0:4] == "talk":
                        send = data.split()

                        if send[1] in CNCT_NAME:
                            rcv = CONNECTION_LIST[CNCT_NAME.index(send[1]) + 1]
                            rcv.send("talk request from " + sender + "(Accept/Reject)\n")
                            data = rcv.recv(4096)

                            if data == "Accept\n":
                                sock.send('Your request is accepted\n')
                                socket_list = [sock, rcv]
                                msg = "\0"
                                while msg != "quit\n":
                                    r_sockets, w_sockets, e_sockets = select.select(socket_list , [], [])
                                    for sockets in r_sockets:
                                        msg = sockets.recv(4096)
                                        if msg == "quit\n":
                                            sock.send('\0')
                                            break
                                        if sockets == sock:
                                            rcv.send(msg)
                                            sock.send('\0')
                                        else:
                                            sock.send(msg)
                                            rcv.send('\0')
                                rcv.send('Stop talk with %s\n' % sender)
                                sock.send('Stop talk with %s\n' % send[1])

                            elif data == "Reject\n":
                                sock.send('Your request is rejected\n')
                        else:
                            sock.send('talk request failed\n')

                    elif data[0:9] == "broadcast":
                    	send = data.split()
                    	broadcast_data(sock, send[1] + " (from " + sender + ")\n")
                        sock.send("\0")

                    elif data == "logout\n":
                        sender = CNCT_NAME[CONNECTION_LIST.index(sock) - 1]
                        print "logout Client %s is offline" % sender
                        sock.close()
                        CNCT_NAME.remove(sender)
                        CONNECTION_LIST.remove(sock)

                    elif data == "change password\n":
                        sock.send('old password:')
                        data = sock.recv(4096)
                        data = data.rstrip('\n')
                        if data == password[CONNECTION_LIST.index(sock) - 1]:
                            sock.send('new password:')
                            np = sock.recv(4096)
                            np = np.rstrip('\n')
                            password[CONNECTION_LIST.index(sock) - 1] = np
                            sock.send('change successful\n')
                        else:
                            sock.send('password is wrong\n')


                except: #if ctrl-c?
                    print "except Client %s is offline" % sender
                    sock.close()
                    CNCT_NAME.remove(sender)
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()
