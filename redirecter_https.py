import http.server
import socketserver

class myHandler(http.server.SimpleHTTPRequestHandler):
   def do_GET(self):
       self.send_response(301)
       self.send_header('Location','https://fifaexperts.com')
       self.end_headers()

PORT = 80
handler = socketserver.TCPServer(("", PORT), myHandler)
handler.serve_forever()
