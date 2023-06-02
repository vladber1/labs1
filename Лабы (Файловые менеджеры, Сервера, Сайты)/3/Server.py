import socket

HOST = 'localhost'
PORT = 5555


def handle_client(conn, addr):
    print(f'Connected by {addr}')
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode()
        if message == "exit":
            break
        print(f'Received from {addr}: {message}')
        conn.send(data)
    print(f'Connection closed by {addr}')
    conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server started on {HOST}:{PORT}')
    while True:
        conn, addr = s.accept()
        handle_client(conn, addr)
