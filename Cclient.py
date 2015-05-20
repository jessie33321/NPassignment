# telnet program example
import getpass, socket, select, string, sys

def prompt() :
    sys.stdout.write('<%s> ' % mode)
    sys.stdout.flush() 

#main function
if __name__ == "__main__":

    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    mode = 'command'
	
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    # login
    data = s.recv(4096)
    sys.stdout.write(data)
    sys.stdout.flush()
    acc = sys.stdin.readline()
    s.send(acc)
    
    data = s.recv(4096)
    sys.stdout.write(data)
    sys.stdout.flush()
    if data == "password:":
        pas = getpass.getpass("")
        #pas = sys.stdin.readline()
        s.send(pas)
    else:
        sys.exit()

    data = s.recv(4096)
    sys.stdout.write(data)
    sys.stdout.flush()
    if data == "login successful\n":
        prompt()        
    else:
        sys.exit()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    sys.stdout.flush()
                    if data == "Your request is accepted\n":
                        mode = "chat"
                    elif data[0:14] == "Stop talk with":
                        mode = "command"
                    if data[-1] != ":":
                        prompt()

            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg)
                if msg == "Accept\n":
                    mode = "chat"
                    prompt()
                elif msg[0:14] == "Stop talk with":
                    mode = "command"
                    prompt()
                elif msg == "Reject\n":
                    prompt()
