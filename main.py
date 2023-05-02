from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
from textparser import textParser

HOST = ''
PORT= 8279

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes("<html><body><h1>Jerry's Rokt Parser</h1></body></html>", "utf-8"))
        else:
            responseList = []
            self.send_error_response(responseList)

    def do_POST(self):
        if self.path == '/':
            # make error validations here
            responseList = []
            try:
                rawString = self.rfile.read(int(self.headers.get('Content-Length')))
                params = json.loads(rawString)
                filePath = params["filename"]
                fromDate = params["from"]
                toDate = params["to"]

                datetime.fromisoformat(fromDate.replace('Z', '+00:00'))
                datetime.fromisoformat(toDate.replace('Z', '+00:00'))

                responseList = textParser.assemble_List(filePath, fromDate, toDate)
                # # return JSON list to terminal
                # send success response
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                jsonString = json.dumps(responseList, indent=2)
                self.wfile.write(bytes(jsonString, "utf-8"))
                self.wfile.write(bytes("\n", "utf8"))
            except:
                self.send_error_response(responseList)
        else:
            responseList = []
            self.send_error_response(responseList)

    def send_error_response(self, responseList):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        jsonString = json.dumps(responseList)
        self.wfile.write(bytes(jsonString, "utf-8"))
        self.wfile.write(bytes("\n", "utf8"))


server = HTTPServer((HOST, PORT), handler)
print("Server is running...")
server.serve_forever()
server.server_close() 
print("Stopped Server!")