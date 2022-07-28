import json
import random
import selectors
import socket

from config import HOST, PORT


def handle(sock, addr):
    try:
        data = sock.recv(1024)  # Should be ready
    except ConnectionError:
        print(f"Client suddenly closed while receiving")
        return False
    print(f"Received {data} from: {addr}")
    if not data:
        print("Disconnected by", addr)
        return False
    data = json.loads(data.decode())
    data = {k: v + random.randint(1, 1000) for k, v in
            data.items()}
    print(f"Send: {data} to: {addr}")
    try:
        sock.send(json.dumps(data, indent=2).encode())  # Hope it won't block
    except ConnectionError:
        print(f"Client suddenly closed, cannot send")
        return False
    return True


def on_connect(sock, addr):
    print("Connected by", addr)


def on_disconnect(sock, addr):
    print("Disconnected by", addr)


def run_server(host, port, on_connect, on_read, on_disconnect):
    def on_accept_ready(sel, serv_sock, mask):
        sock, addr = serv_sock.accept()  # Should be ready
        # sock.setblocking(False)
        sel.register(sock, selectors.EVENT_READ, on_read_ready)
        if on_connect:
            on_connect(sock, addr)

    def on_read_ready(sel, sock, mask):
        addr = sock.getpeername()
        if not on_read or not on_read(sock, addr):
            if on_disconnect:
                on_disconnect(sock, addr)
            sel.unregister(sock)
            sock.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((host, port))
        serv_sock.listen(1)
        # sock.setblocking(False)
        sel = selectors.DefaultSelector()
        sel.register(serv_sock, selectors.EVENT_READ, on_accept_ready)
        while True:
            print("Waiting for connections or data...")
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(sel, key.fileobj, mask)


if __name__ == "__main__":
    run_server(HOST, PORT, on_connect, handle, on_disconnect)
