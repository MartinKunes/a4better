import socket
import json
from threading import Thread

class UDPServer(Thread):
    def __init__(self, config):
        Thread.__init__(self)
        self.peer_id = config.get('peer_id')
        self.address = config.get('udp_server_address')
        self.port = config.get('udp_server_port')
        self.peers = {}
        self.addresses = []

    def run(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.address, self.port))
            while True:
                data, addr = sock.recvfrom(1024)
                message = json.loads(data)
                if 'command' in message and 'peer_id' in message:
                    if message['command'] == 'hello' and message['peer_id'] != self.peer_id:
                        print(f"Received 'hello' from {message['peer_id']}")
                        self.peers[message['peer_id']] = addr
                        self.addresses.append(addr)
                        sock.sendto(json.dumps({"status": "ok", "peer_id": self.peer_id}).encode(), addr)
                        print(f"Sent 'ok' to {message['peer_id']}")
        except Exception as e:
            print(f"Exception in udp_server: {e}")