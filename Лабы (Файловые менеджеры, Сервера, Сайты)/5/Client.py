import socket
import random
import sys

HOST = 'localhost'
PORT = 5555
MAX_BYTES = 1024


def dh_keygen(p, g, a):
    # генерация секретного ключа
    x = random.randint(1, p - 1)
    # вычисление публичного ключа
    y = pow(g, x, p)
    # вычисление общего секретного ключа
    k = pow(a, x, p)
    return k, y


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # получение публичного ключа сервера и отправка своего публичного ключа
    data = s.recv(MAX_BYTES)
    server_pubkey = int(data.decode())
    p = int(input('Enter prime number: '))
    g = int(input('Enter generator: '))
    _, client_pubkey = dh_keygen(p, g, 0)
    s.sendall(str(client_pubkey).encode())
    # вычисление общего секретного ключа
    shared_key, _ = dh_keygen(p, g, server_pubkey)
    print(f'Shared key: {shared_key}')
    # отправка сообщений
    while True:
        message = input('Enter message: ')
        if message == 'exit' or not message:
            s.sendall('exit'.encode())
            break
        # шифрование сообщения с помощью общего ключа
        ciphertext = bytes([(ord(c) + shared_key) % 256 for c in message])
        # отправка зашифрованного сообщения серверу
        s.sendall(ciphertext)
        # получение ответа от сервера и дешифровка ответа
        data = s.recv(MAX_BYTES)
        plaintext = ''.join([chr((b - shared_key) % 256) for b in data])
        print(f'Received: {plaintext}')
