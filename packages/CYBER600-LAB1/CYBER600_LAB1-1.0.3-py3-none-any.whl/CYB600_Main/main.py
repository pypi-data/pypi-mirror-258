# CYB 600 Lab 1
# Eliana Furmanek

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

# Define the handler to use
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set response status code
        self.send_response(200)

        # Set headers
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        current_time = datetime.now()
        # Define the text to be displayed
        response_text = "The Current Times is:", current_time

        # Send the response content as bytes
        self.wfile.write(f"The Current Times is: {current_time}".encode('utf-8'))


def runthis():
    # Set the port you want to use
    port = 8000

    # Create the server and bind it to the specified port
    with HTTPServer(('localhost', port), MyHandler) as server:
        print(f"Serving on port {port}")
        # Start the server
        server.serve_forever()

if __name__ == "__main__":
    runthis()