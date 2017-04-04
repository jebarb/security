import socket
import threading
import subprocess
from Crypto.Cipher import AES

import secrets

DEBUG = True
HOST = 'localhost'
PORT = 1337

# PKCS#7 padding, for AES
def pad(data, block_size=16):
    if type(data) != bytes:
        raise Exception("Need bytes data!")
    length = block_size - (len(data) % block_size)
    return data + bytes([length]) * length

def unpad(data, block_size=16):
    if type(data) != bytes:
        raise Exception("Need bytes data!")
    return data[:-data[-1]]

def handle(conn, addr):
    aes = AES.new(secrets.aes_key, AES.MODE_CBC, secrets.aes_iv)
    output = bytearray()
    try:
        payload = conn.recv(64)
        plaintext = aes.decrypt(payload)
        plaintext = unpad(plaintext)

        # remember to turn off debug in production!
        print('-----------')
        print('cmd: ', plaintext)
        if DEBUG:
            output.extend(b'[DEBUG] Command: ')
            output.extend(plaintext)
            output.extend(b'\n')

        try:
            # runs plaintext as bash command
            proc = subprocess.run(plaintext, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=True, executable='/bin/rbash', check=False)
            print('stderr:', proc.stderr)
            output.extend(proc.stderr)
            output.extend(proc.stdout)
        except Exception as e:
            print(e)
            output.extend(b'bash threw an error: ')
            output.extend(bytes(str(e), 'ascii'))
            output.extend(b'\n')
    except Exception as e:
        print('Handle fail:', e)
        try:
            output.extend(b'Invalid user input\n')
        except:
            pass
    finally:
        try:
            conn.sendall(output)
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
        except:
            pass

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(50)

    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle, args=(conn, addr)).start()

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print('Exception occurred:', e)
