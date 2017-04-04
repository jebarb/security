import socket
import random

HOST='localhost'
PORT=1337


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print('''!!!!!!!!!!!!!!!!!
Please DO NOT attempt to overload the server.
Please DO NOT attempt to tamper with the server environment.
Please DO NOT attempt to do anything else except exfiltrate "sec.txt".
!!!!!!!!!!!!!!!!!''')

    with open('payload.bin', 'rb') as payload:
        sock.send(payload.read())
    print(sock.recv(1024).decode('ascii', 'ignore'))

    sock.close()

if __name__ == '__main__':
    main()
