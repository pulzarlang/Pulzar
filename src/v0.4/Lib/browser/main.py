from http.server import HTTPServer, BaseHTTPRequestHandler


class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        if self.path == '/':
            self.path = '/index.html'

        elif self.path[-1:] == "/":
            self.path += '/index.html'

        if self.path[-4:] == ".plz":
            print("Pulzar file")
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "Error 404 File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))
