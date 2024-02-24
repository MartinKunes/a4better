from config import Config
from udp_server import UDPServer
from udp_client import UDPClient
from tcp_server import TCPServer
from tcp_client import TCPClient
from http_server import HTTPServer

config = Config('config.json')

chat_history = {}
addresses = []

udp_server = UDPServer(config)
udp_client = UDPClient(config)
tcp_server = TCPServer(config, chat_history)
tcp_client = TCPClient(config, addresses, chat_history)
http_server = HTTPServer(config, chat_history, tcp_client)

udp_server.start()
udp_client.start()
tcp_server.start()
tcp_client.start()
http_server.start()