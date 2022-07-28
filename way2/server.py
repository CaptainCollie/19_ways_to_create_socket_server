import json
import socket
import random

from config import HOST, PORT

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen(1)
        print("Server started")
        # Accepting multiple connections, but only one at a time
        while True:  # New
            print("Waiting for connection...")
            sock, addr = serv_sock.accept()
            with sock:
                print("Connected by", addr)
                while True:
                    # Receive
                    try:  # New
                        data_bytes = sock.recv(1024)
                    except ConnectionError:
                        print(f"Client suddenly closed while receiving")
                        break
                    print(f"Received: {data_bytes} from: {addr}")
                    if not data_bytes:
                        break
                    # Process
                    if data_bytes == b"close":
                        break
                    data = json.loads(data_bytes.decode())
                    data = {k: v + random.randint(1, 1000) for k, v in
                            data.items()}
                    # Send
                    print(f"Send: {data} to: {addr}")
                    try:  # New
                        # Uncomment to test exception:
                        # 1) Send data from client and close it
                        # 2) Go to server process and press Enter
                        # 3) Trying to send data to closed client, which cause exception
                        # input("(press enter to send...)")
                        sock.sendall(data)
                    except ConnectionError:
                        print(f"Client suddenly closed, cannot send")
                        break
                print("Disconnected by", addr)
