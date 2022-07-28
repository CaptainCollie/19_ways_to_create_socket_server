import json
import random
import socket
from string import ascii_lowercase

from config import HOST, PORT


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    data = {letter: random.randint(1, 1000) for letter in ascii_lowercase}
    print('Sent', data)
    data_bytes = json.dumps(data, indent=2).encode()
    sock.sendall(data_bytes)
    data_bytes = sock.recv(1024)
    data = json.loads(data_bytes.decode())
    print("Received:", data)
