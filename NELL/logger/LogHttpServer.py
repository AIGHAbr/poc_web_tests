import http.server
import json
import socketserver

from NELL.logger.Logger import Logger


class LogHttpServer(socketserver.TCPServer):
    allow_reuse_address = True


class LogHttpHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        log_data = json.loads(post_data.decode('utf-8'))

        for entry in log_data:
            print(f"[HTTP LOGGER] {entry}")
            Logger.log_event(entry)

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


def start_server(port=8000):
    server = LogHttpServer(("", port), LogHttpHandler)
    with server as httpd:
        print(f"Serving at port {port}")
        try:
            httpd.serve_forever()
        except Exception as e:
            print(f"Server Start Error: {e}")