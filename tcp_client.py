import socket
import json
from threading import Thread

class TCPClient(Thread):
    def __init__(self, config, addresses, chat_history):
        Thread.__init__(self)
        self.peer_id = config.get('peer_id')
        self.addresses = addresses
        self.chat_history = chat_history

    def run(self):
        try:
            for addr in self.addresses:
                print(f"Connected to {addr}")
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(addr)
                    sock.send(json.dumps({"command": "hello", "peer_id": self.peer_id}).encode())
                    data = sock.recv(1024)
                    message = json.loads(data)
                    if isinstance(message, dict):
                        if message['status'] == 'ok':
                            print(f"Received 'ok' from {self.peer_id}")
                            if 'messages' in message:
                                for msg_id, msg in message['messages'].items():
                                    if msg_id not in self.chat_history:
                                        self.chat_history[msg_id] = msg
                            elif 'message_id' in message:
                                self.chat_history[message['message_id']] = {"peer_id": message['peer_id'], "message": message['message']}
                    else:
                        print(f"EXCEPTION: tcp_client: {self.peer_id}: expected dictionary, got {type(message)}")
                    sock.close()
                except ConnectionError:
                    print(f"EXCEPTION: tcp_client: {self.peer_id}: connection closed")
        except Exception as e:
            print(f"Exception in tcp_client: {e}")