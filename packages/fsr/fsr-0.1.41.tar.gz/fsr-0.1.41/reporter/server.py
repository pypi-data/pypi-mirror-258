import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser

def start_server(directory='test_report', port=8080):
    if not directory or not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return

    os.chdir(directory)

    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

    print(f"Serving directory '{directory}' at http://localhost:{port}")
    webbrowser.open(f'http://localhost:{port}', new=2)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped by user")
        httpd.server_close()

if __name__ == "__main__":
    start_server()
