import http.server
import socketserver
import argparse
import logging

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) :
        logging.info(f"GET request,\nPath:{self.path}\nHeaders:\n{self.headers}\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello,Get request received!')

        def do_Post(self):
            content_length=int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            logging.info(f"POST request,\nPath:{self.path}\nHeaders:\n{self.headers}\n\nBody:\n{post_data.decode('utf-8')}\n")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello,POST request received!')

            def do_DELETE(self):
                logging.info(f"DELETE request,\npath:{self.path}\nHeaders:\n{self.headers}\n")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Hello,DELETE request received!')

                def run(server_class=http.server.HTTPServer,handler_class=SimpleHTTPRequestHandler):
                    parser= argparse.ArgumentParser(description='Start the TCP server.')
                    parser.add_argument('--host',default='localhost',help='Hostname to bind to')
                    parser.add_argument('--port',type=int,default=8080,help=Port to bind to')
                    parser.add_argument('--logfile',default='server.log',help='Log file path')
                    args= parser.parse_args()

                    logging.basicConfig(filename=args.logfile,level=logging.INFO)
                    server_address= (args.host,args.port)
                    httpd=server_class(server_adress,handler_class)
                    logging.info(f'Starting httpd server on{args.host}:{args.port}')
                    httpd.serve_forever()

                    if__name__== '__main__':
                    run()

