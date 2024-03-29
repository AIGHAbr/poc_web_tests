import json
import logging
import http.server
import socketserver
import traceback
from NELL.logger.Logger import Logger

class LoggerHolder():

    singleton = None

    def __init__(self, logger=None):
        LoggerHolder.singleton = self
        if logger is None: logger = Logger
        self.logger = logger

    @classmethod
    def get(cls, logger=None):
        if cls.singleton is None:
            cls.singleton = LoggerHolder(logger)
        return cls.singleton
    

    def log_event(self, event):
        self.logger.log_event(event)


class LogHttpServer(socketserver.TCPServer):
    allow_reuse_address = True
    log = logging.getLogger()
    log.setLevel(logging.ERROR)


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

            if not isinstance(log_data, list):
                log_data = [log_data]

            for entry in log_data:
                LoggerHolder.get().log_event(entry)            

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

        except BrokenPipeError as e:
            traceback.print_exc()
            print(f"POST ERROR: {e}")

        except Exception as e:
            traceback.print_exc()
            self.send_error(500, str(e))


def start_server(port=8000):
    
    LoggerHolder()
    server = LogHttpServer(("", port), LogHttpHandler)
    with server as httpd:
        print(f"Serving at port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server Stopped by User.")
            pass
        except Exception as e:
            traceback.print_exc()
            print(f"Server Start Error: {e}")
        finally:
            httpd.server_close()