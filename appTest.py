from textparser import textParser
import json
import os
from datetime import datetime
import threading
import time
import unittest
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen
import requests



class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes("<html><body><h1>Jerry's Rokt Parser</h1></body></html>", "utf-8"))
    
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
                # Simulate parsing
                filePath = os.path.join("app/test-files", filePath)
                entry = {
                        "eventTime" : "2020-12-04T11:14:23Z", 
                        "email" : "jane.doe@email.com", 
                        "sessionId" : "2f31eb2c-a735-4c91-a122-b3851bc87355"}
                responseList.append(entry)

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


class TestRequests(unittest.TestCase):
    @classmethod
    def setup(self):
        server = HTTPServer(("", 8279), MyHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        # Wait for the server to come up
        time.sleep(1)
        return server
    
    @classmethod
    def cleanup(self, server):
        server_thread = threading.Thread(target=server.shutdown)
        server_thread.start()
        server.shutdown()

    @classmethod
    def test_get_request(self):
        assert(bytes("Jerry's Rokt Parser", "utf8") in urlopen("http://localhost:8279/").read())

    @classmethod
    def test_post_request_Happy_Case(self):
        payload = {"filename":"sample1.txt", "from":"2020-07-06T23:00:00Z", "to": "2022-07-06T23:00:00Z"}
        response = requests.post('http://localhost:8279', data=json.dumps(payload))
        testList = []
        entry = {
                "eventTime" : "2020-12-04T11:14:23Z", 
                "email" : "jane.doe@email.com", 
                "sessionId" : "2f31eb2c-a735-4c91-a122-b3851bc87355"}
        testList.append(entry)
        assert(200 == response.status_code)
        assert(response.json() == json.loads(json.dumps(testList)))

    @classmethod
    def test_post_request_error_case_sensitive(self):
        payload = {"Filename":"sample1.txt", "From":"2020-07-06T23:00:00Z", "To": "2022-07-06T23:00:00Z"}
        response = requests.post('http://localhost:8279', data=json.dumps(payload))
        testList = []
        assert(200 == response.status_code)
        assert(response.json() == json.loads(json.dumps(testList)))

    @classmethod
    def test_post_request_error_iso8601(self):
        payload = {"filename":"sample1.txt", "from":"07-06-2020T23:00:00Z", "to": "07-06-2022T23:00:00Z"}
        response = requests.post('http://localhost:8279', data=json.dumps(payload))
        testList = []
        assert(200 == response.status_code)
        assert(response.json() == json.loads(json.dumps(testList)))

    @classmethod
    def test_post_request_error_iso8601_two(self):
        payload = {"filename":"sample1.txt", "from":"2020-07-0623:00:00", "to": "2022-07-0623:00:00"}
        response = requests.post('http://localhost:8279', data=json.dumps(payload))
        testList = []
        assert(200 == response.status_code)
        assert(response.json() == json.loads(json.dumps(testList)))
    
    @classmethod
    def test_post_request_error_invalid_HTTP_path(self):
        payload = {"filename":"sample1.txt", "from":"2020-07-06T23:00:00Z", "to": "2022-07-06T23:00:00Z"}
        response = requests.post('http://localhost:8279/invalidPath', data=json.dumps(payload))
        testList = []
        assert(200 == response.status_code)
        assert(response.json() == json.loads(json.dumps(testList)))

print("Starting Tests!")
testServer = TestRequests.setup()
print("Starting test_get_request...")
TestRequests.test_get_request()
print("Starting test_post_request_Happy_Case...")
TestRequests.test_post_request_Happy_Case()
print("Starting test_post_request_error_case_sensitive...")
TestRequests.test_post_request_error_case_sensitive()
print("Starting test_post_request_error_iso8601...")
TestRequests.test_post_request_error_iso8601()
print("Starting test_post_request_error_iso8601_two...")
TestRequests.test_post_request_error_iso8601_two()
print("Starting test_post_request_error_invalid_HTTP_path...")
TestRequests.test_post_request_error_invalid_HTTP_path()

TestRequests.cleanup(testServer)
print("---All Tests Passed---")



