import socket
import threading
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


def handle_client(conn, addr):
    print(f'Connected by {addr}')
    # генерация параметров Диффи-Хеллмана
    p = int(input('Enter prime number: '))
    g = int(input('Enter generator: '))
    # отправка публичного ключа клиенту
    _, server_pubkey = dh_keygen(p, g, 0)
    conn.sendall(str(server_pubkey).encode())
    # получение публичного ключа клиента и вычисление общего секретного ключа
    data = conn.recv(MAX_BYTES)
    client_pubkey = int(data.decode())
    shared_key, _ = dh_keygen(p, g, client_pubkey)
    print(f'Shared key: {shared_key}')
    # получение и отправка сообщений
    while True:
        data = conn.recv(MAX_BYTES)
        message = data.decode()
        if message == "exit":
            break
        # шифрование сообщения с помощью общего ключа
        ciphertext = bytes([(ord(c) + shared_key) % 256 for c in message])
        # отправка зашифрованного сообщения клиенту
        conn.sendall(ciphertext)
    print(f'Connection closed by {addr}')
    conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server started on {HOST}:{PORT}')
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
