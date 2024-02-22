from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Get the current time
        current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

        # Send the response containing the current time
        self.wfile.write("Current time: {}".format(current_time).encode())


def run(server_class=HTTPServer, handler_class=HTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
