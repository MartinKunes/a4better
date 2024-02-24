import socket
import json
from threading import Thread

class TCPServer(Thread):
    def __init__(self, config, chat_history):
        Thread.__init__(self)
        self.peer_id = config.get('peer_id')
        self.address = config.get('tcp_server_address')
        self.port = config.get('tcp_server_port')
        self.chat_history = chat_history

    def run(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.address, self.port))
            sock.listen(1)
            while True:
                conn, addr = sock.accept()
                data = conn.recv(1024)
                print(f"Raw data received: {data}")  # Print raw data
                try:
                    message = json.loads(data)
                    print(f"Parsed message: {message}")  # Print parsed message
                except json.JSONDecodeError:
                    print(f"EXCEPTION: tcp_server: received data is not valid JSON: {data}")
                    continue
                if isinstance(message, dict) and 'status' in message:
                    if message['status'] == 'ok':
                        print(f"Received 'ok' from {addr}")
                    else:
                        print(f"Status is not 'ok': {message['status']}")  # Print status if not 'ok'
                if isinstance(message, dict) and 'command' in message:
                    if message['command'] == 'hello':
                        print(f"Received 'hello' from {addr}")
                        conn.send(json.dumps({"status": "ok", "messages": self.chat_history}).encode())
                        print(f"Sent 'ok' to {addr}")
                    elif message['command'] == 'new_message':
                        self.chat_history[message['message_id']] = message
                        conn.send(json.dumps({"status": "ok"}).encode())
                        print(f"Sent 'ok' to {addr}")
                    else:
                        conn.send(json.dumps({"status": "ok"}).encode())
                conn.close()
        except Exception as e:
            print(f"Exception in tcp_server: {e}")
