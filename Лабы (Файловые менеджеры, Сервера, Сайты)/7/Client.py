import socket
import os

HOST = 'localhost'
PORT = 5555


def list_files():
    message = 'LIST'
    s.send(message.encode())
    data = s.recv(1024)
    print(f'Files in directory: {data.decode()}')


def create_folder():
    folder_name = input('Enter folder name: ')
    message = f'MKDIR {folder_name}'
    s.send(message.encode())
    data = s.recv(1024)
    print(f'Server response: {data.decode()}')


def delete_folder():
    folder_name = input('Enter folder name: ')
    message = f'RMDIR {folder_name}'
    s.send(message.encode())
    data = s.recv(1024)
    print(f'Server response: {data.decode()}')


def delete_file():
    file_name = input('Enter file name: ')
    message = f'DELETE {file_name}'
    s.send(message.encode())
    data = s.recv(1024)
    print(f'Server response: {data.decode()}')


def rename_file():
    old_name = input('Enter old file name: ')
    new_name = input('Enter new file name: ')
    message = f'RENAME {old_name} {new_name}'
    s.send(message.encode())
    data = s.recv(1024)
    print(f'Server response: {data.decode()}')


def copy_to_server():
    file_path = input('Enter local file path: ')
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        data = f.read()
    message = f'UPLOAD {file_name}'
    s.send(message.encode())
    s.sendall(data)
    data = s.recv(1024)
    print(f'Server response: {data.decode()}')


def copy_from_server():
    file_name = input('Enter file name: ')
    message = f'DOWNLOAD {file_name}'
    s.send(message.encode())
    data = s.recv(1024)
    if data.decode() == 'File not found':
        print('Server response: File not found')
    else:
        with open(file_name, 'wb') as f:
            f.write(data)
        print('Server response: File downloaded successfully')


def exit_client():
    message = 'EXIT'
    s.send(message.encode())
    s.close()
    print('Client disconnected')


commands = {
    '1': list_files,
    '2': create_folder,
    '3': delete_folder,
    '4': delete_file,
    '5': rename_file,
    '6': copy_to_server,
    '7': copy_from_server,
    '8': exit_client
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Connected to server')
    while True:
        command = input('Enter command:\n'
                        '1. List files\n'
                        '2. Create folder\n'
                        '3. Delete folder\n'
                        '4. Delete file\n'
                        '5. Rename file\n'
                        '6. Copy to server\n'
                        '7. Copy from server\n'
                        '8. Exit\n')
        if command in commands:
            commands[command]()
        else:
            print('Invalid command')
