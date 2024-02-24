import socket
import json
import time
from threading import Thread

class UDPClient(Thread):
    def __init__(self, config):
        Thread.__init__(self)
        self.peer_id = config.get('peer_id')
        self.broadcast_address = config.get('udp_server_address')
        self.port = config.get('udp_server_port')

    def run(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while True:
                sock.sendto(json.dumps({"command": "hello", "peer_id": self.peer_id}).encode(), (self.broadcast_address, self.port))
                print(f"Sent 'hello' from {self.peer_id}")
                time.sleep(5)
        except Exception as e:
            print(f"Exception in udp_client: {e}")