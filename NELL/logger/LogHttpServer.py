import http.server
import json
import socketserver

from NELL.logger.Logger import Logger


class LogHttpServer(socketserver.TCPServer):
    allow_reuse_address = True


class LogHttpHandler(http.server.SimpleHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            log_data = json.loads(post_data.decode('utf-8'))

            for entry in log_data:
                Logger.log_event(entry)

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
        except BrokenPipeError as e:
            print(f"Erro ao processar POST: {e}")
        except Exception as e:
            self.send_error(500, str(e))


def start_server(port=8000):
    server = LogHttpServer(("", port), LogHttpHandler)
    with server as httpd:
        print(f"Serving at port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Server Start Error: {e}")
        finally:
            httpd.server_close()