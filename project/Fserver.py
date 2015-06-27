#-*- coding: UTF-8 -*-
# Tcp Chat server


import socket, select, time, random

#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket:
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
    record = [0,0,0,0,0,0]

    ques = ['題目:請問高爾夫球的顏色為何\n(1)紫色(2)綠色(3)白色(4)黃色\n'
    ,'題目:請問iPhone的作業系統為何\n(1)andriod(2)android(3)ios(4)linux\n'
    ,'題目:請問下列哪一地區為一級方程式賽車的發源處？\n(1)歐洲(2)非洲(3)美洲(4)皮蛋瘦肉洲\n'
    ,'題目:資訊與通信術語中「美國資訊交換標準碼」的簡稱是什麼？\n(1)UTF-8(2)ASCII(3)ASCI(4)ANSI\n'
    ,'題目:在網路中傳輸的「格式化資料塊」，此一資訊傳輸單位被稱為什麼？\n(1)麵包(2)皮包(3)刈包(4)封包\n'
    ,'題目:「Gmail」是哪一家公司推出的網路郵件服務平台？\n(1)Google(2)Amazon(3)Yahoo(4)Facebook\n'
    ,'題目:下列何者為電腦網際網路的「共通通訊標準協定」?\n(1)DHCP(2)TCP/IP(3)DNS(4)WWW\n'
    ,'題目:台灣流行用語中會將網路論壇「PTT的使用者」稱為什麼？\n(1)鄉民(2)村民(3)人民(4)子民\n'
    ]
    answ = ['3\n'
    ,'3\n'
    ,'1\n'
    ,'2\n'
    ,'4\n'
    ,'1\n'
    ,'2\n'
    ,'1\n']

    score1 = 0
    score2 = 0
    score3 = 0

    twoP = []
    two = 0 

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

                    elif data == "record\n":
                        i = account.index(sender)
                        sock.send(str(record[i*2]) + '勝 ' + str(record[i*2+1]) + '敗\n' )

                    elif data == "1P\n":
                        score1 = 0
                        sock.send('你要幾題啦... 阿最多只能五題哦\n')
                        qnum = sock.recv(RECV_BUFFER)
                        r = range(1,len(ques)+1)
                        print(r)
                        ran = random.sample(r,int(qnum))
                        print(ran)
                        for i in range(0,int(qnum)):
                            msg = '<practice>'+ques[ran[i]]
                            sock.send(msg)
                            d = sock.recv(RECV_BUFFER)
                            print('1 '+d)
                            if d == answ[ran[i]]:
                                sock.send('correct!!\n')
                                score1 = score1+1
                            else:
                                sock.send('wrong!!\n')
                        sock.send('答題率'+str(float(score1)/float(qnum)*100)+'%\n')

                    elif data == "quit 2P\n":
                        two=two-1
                        twoP.remove(sock)
                        sock.send('quit successful!\n')

                    elif data == "2P\n":
                    	two=two+1
                    	twoP.append(sock)
                        if two < 2:
                            msg = "wait for " + str(2-two) + " player\n"
                            sock.send(msg)
                            broadcast_data(sock,'2P' + msg)
                        elif two == 2:
                            score1=0
                            score2=0
                            for i in range(0,2):
                                msg = ques[i]
                                twoP[0].send(msg)
                                twoP[1].send(msg)
                                ans1 = twoP[0].recv(RECV_BUFFER)
                                print('ans1 '+ans1)
                                ans2 = twoP[1].recv(RECV_BUFFER)
                                print('ans2 '+ans2)
                                a1 = ans1.split('\n')
                                a2 = ans2.split('\n')
                                print('spilt OK\n')
                                ans1 = a1[0]+'\n'
                                time1 = a1[2]
                                ans2 = a2[0]+'\n'
                                time2 = a2[2]
                                print('1 '+time1)
                                print('2 '+time2)
                                if ans1 == answ[i]:
                                    twoP[0].send('correct!!\n')
                                    print('time1 '+time1)
                                    if float(time1) <= 3:
                                        score1 = score1+3
                                        print('P1+3')
                                    elif float(time1) <= 5:
                                        score1 = score1+2
                                    else:
                                        score1 = score1+1
                                else:
                                    twoP[0].send('wrong!!\n')
                                if ans2 == answ[i]:
                                    twoP[1].send('correct!!\n')
                                    print('time2 '+time2)
                                    if float(time2) <= 3:
                                        score2 = score2+3
                                        print('P2+3')
                                    elif float(time2) <= 5:
                                        score2 = score2+2
                                    else:
                                        score2 = score2+1

                                else:
                                    twoP[1].send('wrong!!\n')
                                time.sleep(0.5)
                            two = 0
                            print('s1 : '+str(score1)+'s2 : '+str(score2))
                            if score1>score2:
                                twoP[0].send('You win!!\n')
                                twoP[1].send('You lose!!\n')
                                i = account.index(CNCT_NAME[CONNECTION_LIST.index(twoP[0])-1])
                                record[i*2] = record[i*2] + 1
                                i = account.index(CNCT_NAME[CONNECTION_LIST.index(twoP[1])-1])
                                record[i*2+1] = record[i*2+1] + 1
                            elif score1<score2:
                                twoP[1].send('You win!!\n')
                                twoP[0].send('You lose!!\n')
                                i = account.index(CNCT_NAME[CONNECTION_LIST.index(twoP[1])-1])
                                record[i*2] = record[i*2] + 1
                                i = account.index(CNCT_NAME[CONNECTION_LIST.index(twoP[0])-1])
                                record[i*2+1] = record[i*2+1] + 1

                            else:
                                twoP[0].send('Tie!!\n')
                                twoP[1].send('Tie!!\n')	
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
