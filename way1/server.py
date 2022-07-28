import json
import random
import socket

from config import HOST, PORT

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    sock, addr = server_socket.accept()
    with sock:
        print("Connected by", addr)
        while True:
            data_bytes = sock.recv(1024)
            data = json.loads(data_bytes.decode())
            print(f'Received {data} from {addr}')
            data = {k: v + random.randint(1, 1000) for k, v in data.items()}
            print(f'Sent {data} to {addr}')
            data_bytes = json.dumps(data, indent=2).encode()
            sock.sendall(data_bytes)

