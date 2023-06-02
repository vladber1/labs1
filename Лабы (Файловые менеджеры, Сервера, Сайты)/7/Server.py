import socket
import threading
import os

HOST = 'localhost'
PORT = 5555
BASE_DIR = os.getcwd()


def handle_client(conn, addr):
    print(f'Connected by {addr}')
    current_dir = BASE_DIR
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode()
        if message == 'CANCEL':
            break
        elif message == 'LIST':
            files = os.listdir(current_dir)
            conn.send(str(files).encode())
        elif message.startswith('MKDIR'):
            folder_name = message.split()[1]
            try:
                os.mkdir(os.path.join(current_dir, folder_name))
                conn.send('Folder created successfully'.encode())
            except:
                conn.send('Failed to create folder'.encode())
        elif message.startswith('RMDIR'):
            folder_name = message.split()[1]
            try:
                os.rmdir(os.path.join(current_dir, folder_name))
                conn.send('Folder deleted successfully'.encode())
            except:
                conn.send('Failed to delete folder'.encode())
        elif message.startswith('DELETE'):
            file_name = message.split()[1]
            try:
                os.remove(os.path.join(current_dir, file_name))
                conn.send('File deleted successfully'.encode())
            except:
                conn.send('Failed to delete file'.encode())
        elif message.startswith('RENAME'):
            old_name = message.split()[1]
            new_name = message.split()[2]
            try:
                os.rename(os.path.join(current_dir, old_name), os.path.join(current_dir, new_name))
                conn.send('File renamed successfully'.encode())
            except:
                conn.send('Failed to rename file'.encode())
        elif message.startswith('UPLOAD'):
            file_name = message.split()[1]
            data = conn.recv(1024)
            with open(os.path.join(current_dir, file_name), 'wb') as f:
                f.write(data)
            conn.send('File uploaded successfully'.encode())
        elif message.startswith('DOWNLOAD'):
            file_name = message.split()[1]
            try:
                with open(os.path.join(current_dir, file_name), 'rb') as f:
                    data = f.read()
                conn.sendall(data)
            except:
                conn.send('File not found'.encode())
        else:
            conn.send('Invalid command'.encode())
    print(f'Connection closed by {addr}')
    conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server started on {HOST}:{PORT}')
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

# xd0x92xd0x9bxd0x90xd0x94xd0xa7xd0x9bxd0x95xd0x9d
