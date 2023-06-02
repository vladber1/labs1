import socket

filename = input("Enter file name (Example: index.html): ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind(('', 80))
    except OSError:
        s.bind(('', 8080))

    s.listen(5)

    conn, addr = s.accept()
    print("Connected", addr)

    data = conn.recv(8192)
    msg = data.decode()

    with open(filename) as f:
        content = f.read()

    resp = """HTTP/1.1 200 OK
    Hello, webworld!"""

    resp = content + "Hello, webworld!"

    conn.sendall(resp.encode())

    conn.close()
