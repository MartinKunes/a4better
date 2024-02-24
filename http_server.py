import http.server
import socketserver
import json
import time
from threading import Thread

class HTTPServer(Thread):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, chat_history=None, tcp_client=None, **kwargs):
            self.chat_history = chat_history
            self.tcp_client = tcp_client
            super().__init__(*args, **kwargs)

        def do_POST(self):
            try:
                if self.path == '/send':
                    length = int(self.headers.get('content-length'))
                    message = json.loads(self.rfile.read(length))
                    message_id = str(time.time())
                    self.chat_history[message_id] = {"peer_id": self.peer_id, "message": message}
                    self.tcp_client(message)
                    self.send_response(200)
                    self.end_headers()
            except Exception as e:
                print(f"Exception in HTTP server: {e}")

    def __init__(self, config, chat_history, tcp_client):
        Thread.__init__(self)
        self.port = config.get('http_server_port')
        self.chat_history = chat_history
        self.tcp_client = tcp_client

    def run(self):
        try:
            with socketserver.TCPServer(('', self.port), lambda *args, **kwargs: self.Handler(*args, chat_history=self.chat_history, tcp_client=self.tcp_client, **kwargs)) as httpd:
                httpd.serve_forever()
        except Exception as e:
            print(f"Exception in http_server: {e}")